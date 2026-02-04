from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from decimal import Decimal

from app.core.database import get_db
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.product import Product
from app.models.supplier import Supplier



from app.services.purchase_service import (
    generate_purchase_number_service,
    calculate_purchase_totals_service,
    create_purchase_service,
    list_purchases_service,
    list_purchase_by_id_service,
    PurchaseNotFoundError,
    SupplierNotFoundError,
    update_purchase_service,
    delete_purchase_service,
    ProductNotFoundError
) 

from app.services.supplier_service import (
    validate_supplier_exists_service
)

from app.schemas.purchase import (
    PurchaseItemResponse,
    PurchaseResponse,
    PurchaseCreate,
    PurchaseUpdate
) 

from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=PurchaseResponse, status_code=status.HTTP_201_CREATED)
def create_purchase(
    purchase_data: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    supplier = validate_supplier_exists_service(db, purchase_data.supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with ID {purchase_data.supplier_id} not found"
        )

    try:
        
        return create_purchase_service(db, purchase_data, current_user.id)

    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {e.product_id} not found"
        )



@router.get("/", response_model=List[PurchaseResponse])
def list_purchases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all purchases ordered by creation date (newest first)"""
    purchases = list_purchases_service(db)
    return purchases


@router.get("/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single purchase by ID with all items"""
    purchase = list_purchase_by_id_service(db, purchase_id)
    
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase with ID {purchase_id} not found"
        )
    
    return purchase


@router.put("/{purchase_id}", response_model=PurchaseResponse)
def update_purchase(
    purchase_id: int,
    purchase_data: PurchaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return update_purchase_service(db, purchase_id, purchase_data)

    except PurchaseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase with ID {purchase_id} not found"
        )

    except SupplierNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with ID {e.supplier_id} not found"
        )

    except ProductNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {e.product_id} not found"
        )

    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Database integrity error"
        )

@router.delete("/{purchase_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        delete_purchase_service(db, purchase_id)
        return

    except PurchaseNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Purchase with ID {purchase_id} not found"
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting purchase"
        )


