from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models import Purchase, PurchaseItem, Product
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.models.user import User

router = APIRouter()

# Incrementa el stock
@router.post("/", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(
    data: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    purchase = Purchase(
        supplier_id=data.supplier_id,
        user_id=current_user.id,
        total_amount=0
    )

    db.add(purchase)
    db.flush()  # obtener purchase.id

    total = 0

    for item in data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product ID {item.product_id} not found"
            )

        subtotal = item.quantity * item.unit_cost
        total += subtotal

        # Incrementar stock
        product.stock_quantity += item.quantity

        purchase_item = PurchaseItem(
            purchase_id=purchase.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_cost=item.unit_cost,
            subtotal=subtotal
        )

        db.add(purchase_item)

    purchase.total_amount = total

    db.commit()
    db.refresh(purchase)

    return purchase

# Lista compras
@router.get("/", response_model=List[PurchaseResponse])
def list_purchases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Purchase).order_by(Purchase.created_at.desc()).all()
