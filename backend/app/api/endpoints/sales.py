
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.schemas.sale import SaleCreate, SaleResponse
from app.api.deps import get_current_user
from app.models.user import User
from typing import List

router = APIRouter()

@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not sale_data.items:
        raise HTTPException(400, "Sale must have at least one item")

    sale = Sale(
        user_id=current_user.id,
        total_amount=0
    )

    db.add(sale)
    db.flush()  # obtener sale.id sin commit

    total = 0
    sale_items = []

    for item in sale_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(404, f"Product {item.product_id} not found")

        if product.stock_quantity < item.quantity:
            raise HTTPException(
                400,
                f"Not enough stock for {product.name}"
            )

        subtotal = float(product.price) * item.quantity
        total += subtotal

        # Descontar stock
        product.stock_quantity -= item.quantity

        sale_item = SaleItem(
            sale_id=sale.id,
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            subtotal=subtotal
        )

        sale_items.append(sale_item)

    sale.total_amount = total
    db.add_all(sale_items)
    db.commit()
    db.refresh(sale)

    return sale

@router.get("/", response_model=List[SaleResponse])
def get_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Sale).order_by(Sale.created_at.desc()).all()

