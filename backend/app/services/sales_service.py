from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from typing import List
from decimal import Decimal
from datetime import date

from app.core.database import get_db
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.client import Client
from app.schemas.sale import SaleCreate, SaleUpdate, SaleResponse
from app.api.deps import get_current_user
from app.models.user import User



def generate_sale_number_service(db: Session) -> str:
    """Generate a unique sale number"""
    # Get the last sale number
    last_sale = db.query(Sale).order_by(Sale.id.desc()).first()
    if last_sale and last_sale.sale_number:
        # Extract number from format like "SALE-00001"
        try:
            last_num = int(last_sale.sale_number.split("-")[-1])
            new_num = last_num + 1
        except (ValueError, IndexError):
            new_num = 1
    else:
        new_num = 1
    
    return f"SALE-{new_num:05d}"


def calculate_sale_totals_service(items: List[SaleItem]) -> dict:
    """Calculate subtotal, tax, discount, and total for a sale"""
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

class SaleNotFoundError(Exception):
    pass


class ClientNotFoundError(Exception):
    pass


class ProductNotFoundError(Exception):
    def __init__(self, product_id: int):
        self.product_id = product_id


class InsufficientStockError(Exception):
    def __init__(self, product_name: str, available: int, requested: int):
        self.product_name = product_name
        self.available = available
        self.requested = requested


def create_sale_service(db: Session, sale_data, current_user):
    # Validate client exists
    client = db.query(Client).filter(Client.id == sale_data.client_id).first()
    if not client:
        raise ClientNotFoundError()

    sale = Sale(
        sale_number=sale_data.sale_number,
        client_id=sale_data.client_id,
        user_id=current_user.id,
        sale_date=sale_data.sale_date,
        due_date=sale_data.due_date,
        status=sale_data.status or "pending",
        payment_status=sale_data.payment_status or "unpaid",
        notes=sale_data.notes,
        subtotal=Decimal("0.00"),
        tax=Decimal("0.00"),
        discount=Decimal("0.00"),
        total=Decimal("0.00")
    )

    db.add(sale)
    db.flush()

    sale_items = []

    for item_data in sale_data.items:
        product = db.query(Product).filter(Product.id == item_data.product_id).first()
        if not product:
            raise ProductNotFoundError(item_data.product_id)

        if product.stock_quantity < item_data.quantity:
            raise InsufficientStockError(
                product.name,
                product.stock_quantity,
                item_data.quantity
            )

        subtotal = Decimal(str(item_data.quantity)) * item_data.unit_price
        product.stock_quantity -= item_data.quantity

        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            subtotal=subtotal
        )

        sale_items.append(sale_item)

    db.add_all(sale_items)

    return sale, sale_items


def get_sale_service(db: Session, sale_id: int) -> Sale:
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise SaleNotFoundError()
    return sale


def list_sales_service(db: Session):
    return db.query(Sale).order_by(Sale.created_at.desc()).all()


def update_sale_service(db: Session, sale_id: int, sale_data):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise SaleNotFoundError()

    if sale_data.client_id is not None:
        client = db.query(Client).filter(Client.id == sale_data.client_id).first()
        if not client:
            raise ClientNotFoundError()
        sale.client_id = sale_data.client_id

    for field in ["sale_number", "sale_date", "due_date", "status", "payment_status", "notes"]:
        value = getattr(sale_data, field)
        if value is not None:
            setattr(sale, field, value)

    if sale_data.items is not None:
        old_items = db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()
        for old_item in old_items:
            product = db.query(Product).filter(Product.id == old_item.product_id).first()
            if product:
                product.stock_quantity += old_item.quantity

        db.query(SaleItem).filter(SaleItem.sale_id == sale_id).delete()
        db.flush()

        new_items = []

        for item_data in sale_data.items:
            product = db.query(Product).filter(Product.id == item_data.product_id).first()
            if not product:
                raise ProductNotFoundError(item_data.product_id)

            if product.stock_quantity < item_data.quantity:
                raise InsufficientStockError(
                    product.name,
                    product.stock_quantity,
                    item_data.quantity
                )

            subtotal = Decimal(str(item_data.quantity)) * item_data.unit_price
            product.stock_quantity -= item_data.quantity

            new_items.append(
                SaleItem(
                    sale_id=sale.id,
                    product_id=product.id,
                    quantity=item_data.quantity,
                    unit_price=item_data.unit_price,
                    subtotal=subtotal
                )
            )

        db.add_all(new_items)
        return sale, new_items

    return sale, None


def delete_sale_service(db: Session, sale_id: int):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if not sale:
        raise SaleNotFoundError()

    items = db.query(SaleItem).filter(SaleItem.sale_id == sale_id).all()
    for item in items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            product.stock_quantity += item.quantity

    db.delete(sale)
