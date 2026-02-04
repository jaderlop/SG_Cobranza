from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from decimal import Decimal

from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.product import Product
from app.models.supplier import Supplier

from app.schemas.purchase import (
    PurchaseCreate, 
    PurchaseUpdate, 
    PurchaseResponse
)
from app.models.purchase_item import PurchaseItem

class PurchaseServiceError(Exception):
    pass

class SupplierNotFoundError(PurchaseServiceError):
    pass

class ProductNotFoundError(PurchaseServiceError):
    pass

class PurchaseNotFoundError(PurchaseServiceError):
    pass

class ProductNotFoundError(PurchaseServiceError):
    def __init__(self, product_id: int):
        self.product_id = product_id


def generate_purchase_number_service(db: Session) -> str:
    """Generate a unique purchase number"""
    # Get the last purchase number
    last_purchase = db.query(Purchase).order_by(Purchase.id.desc()).first()
    if last_purchase and last_purchase.purchase_number:
        # Extract number from format like "PURCHASE-00001"
        try:
            last_num = int(last_purchase.purchase_number.split("-")[-1])
            new_num = last_num + 1
        except (ValueError, IndexError):
            new_num = 1
    else:
        new_num = 1
    
    return f"PURCHASE-{new_num:05d}"


def calculate_purchase_totals_service(items: List[PurchaseItem]) -> dict:
    """Calculate subtotal, tax, discount, and total for a purchase"""
    subtotal = sum(item.subtotal for item in items)
    tax = Decimal("0.00")  # For now, no tax
    discount = Decimal("0.00")  # For now, no discount
    total = subtotal + tax - discount
    
    return {
        "subtotal": subtotal,
        "tax": tax,
        "discount": discount,
        "total": total
    }

def create_purchase_service(
    db: Session,
    purchase_data: PurchaseCreate,
    user_id: int
) -> Purchase:
    """Create a new purchase with items"""
  
    purchase_number = purchase_data.purchase_number or generate_purchase_number_service(db)

    try:
        purchase = Purchase(
            purchase_number=purchase_number,
            supplier_id=purchase_data.supplier_id,
            user_id=user_id,
            purchase_date=purchase_data.purchase_date or date.today(),
            due_date=purchase_data.due_date,
            status=purchase_data.status or "pending",
            notes=purchase_data.notes,
            subtotal=Decimal("0.00"),
            tax=Decimal("0.00"),
            discount=Decimal("0.00"),
            total=Decimal("0.00")
        )
    
        db.add(purchase)
        db.flush()

        purchase_items: List[PurchaseItem] = []

        # Process each item
        for item_data in purchase_data.items:
                #Validate product exists
                product = db.query(Product).filter(Product.id == item_data.product_id).first()
                if not product:
                    raise ProductNotFoundError(item_data.product_id)
                
                ## Caculate subtotal for intem
                subtotal = Decimal(str(item_data.quantity)) * item_data.unit_price
                product.stock_quantity += item_data.quantity
                
                ## Create prucase item
                purchase_items.append(
                    PurchaseItem(
                        purchase_id=purchase.id,
                        product_id=product.id,
                        quantity=item_data.quantity,
                        unit_price=item_data.unit_price,
                        subtotal=subtotal
                    )
                )

        db.add_all(purchase_items)

        totals = calculate_purchase_totals_service(purchase_items)
        purchase.subtotal = totals["subtotal"]
        purchase.tax = totals["tax"]
        purchase.discount = totals["discount"]
        purchase.total = totals["total"]

        db.commit()
        db.refresh(purchase)
        return purchase

    except:
        db.rollback()
        raise

def list_purchases_service(db: Session):
    """List all purchases ordered by creation date (newest first)"""
    purchases = db.query(Purchase).order_by(Purchase.created_at.desc()).all()
    return purchases

def list_purchase_by_id_service(
    db: Session,
    purchase_id: int,
):
    """Get a purchase by ID"""
    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    return purchase

def update_purchase_service(
    db: Session,
    purchase_id: int,
    purchase_data: PurchaseUpdate
) -> Purchase:

    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise PurchaseNotFoundError()

    # Update basic fields
    if purchase_data.purchase_number is not None:
        purchase.purchase_number = purchase_data.purchase_number

    if purchase_data.supplier_id is not None:
        supplier = db.query(Supplier).filter(Supplier.id == purchase_data.supplier_id).first()
        if not supplier:
            raise SupplierNotFoundError(purchase_data.supplier_id)
        purchase.supplier_id = purchase_data.supplier_id

    if purchase_data.purchase_date is not None:
        purchase.purchase_date = purchase_data.purchase_date

    if purchase_data.due_date is not None:
        purchase.due_date = purchase_data.due_date

    if purchase_data.status is not None:
        purchase.status = purchase_data.status

    if purchase_data.notes is not None:
        purchase.notes = purchase_data.notes

    # If items are provided, update them
    if purchase_data.items is not None:
        # Reverse stock from old items
        old_items = db.query(PurchaseItem).filter(PurchaseItem.purchase_id == purchase_id).all()
        for old_item in old_items:
            product = db.query(Product).filter(Product.id == old_item.product_id).first()
            if product:
                product.stock_quantity -= old_item.quantity

        # Delete old items
        db.query(PurchaseItem).filter(PurchaseItem.purchase_id == purchase_id).delete()
        db.flush()

        new_purchase_items = []

        for item_data in purchase_data.items:
            product = db.query(Product).filter(Product.id == item_data.product_id).first()
            if not product:
                raise ProductNotFoundError(item_data.product_id)

            subtotal = Decimal(str(item_data.quantity)) * item_data.unit_price
            product.stock_quantity += item_data.quantity

            new_purchase_items.append(
                PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=product.id,
                    quantity=item_data.quantity,
                    unit_price=item_data.unit_price,
                    subtotal=subtotal
                )
            )

        db.add_all(new_purchase_items)

        totals = calculate_purchase_totals_service(new_purchase_items)
        purchase.subtotal = totals["subtotal"]
        purchase.tax = totals["tax"]
        purchase.discount = totals["discount"]
        purchase.total = totals["total"]

    db.commit()
    db.refresh(purchase)
    return purchase

def delete_purchase_service(db: Session, purchase_id: int) -> None:
    """
    Delete a purchase and reverse stock.

    Business logic:
    - Reverse stock for all purchase items
    - Delete purchase (cascade deletes items)
    """

    purchase = db.query(Purchase).filter(Purchase.id == purchase_id).first()
    if not purchase:
        raise PurchaseNotFoundError()

    # Reverse stock from items
    items = db.query(PurchaseItem).filter(PurchaseItem.purchase_id == purchase_id).all()
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_quantity -= item.quantity

    db.delete(purchase)
    db.commit()