from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from decimal import Decimal
from datetime import date

from app.services.sales_service import (
    generate_sale_number_service,
    calculate_sale_totals_service,
    SaleNotFoundError,
    ClientNotFoundError,
    ProductNotFoundError,
    InsufficientStockError,
    create_sale_service,
    get_sale_service,
    list_sales_service,
    update_sale_service,
    delete_sale_service
)

from app.core.database import get_db
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.product import Product
from app.models.client import Client
from app.schemas.sale import SaleCreate, SaleUpdate, SaleResponse
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


@router.post("/", response_model=SaleResponse, status_code=status.HTTP_201_CREATED)
def create_sale(
    sale_data: SaleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new sale with items.
    
    Business logic:
    - Validates all products exist
    - Checks stock availability
    - Calculates subtotal for each item (quantity * unit_price)
    - Calculates total for sale (sum of all subtotals)
    - Decrements product stock
    - Creates sale and all items in a transaction
    """
    try:
        sale, items = create_sale_service(db, sale_data, current_user)
        totals = calculate_sale_totals_service(items)

        sale.subtotal = totals["subtotal"]
        sale.tax = totals["tax"]
        sale.discount = totals["discount"]
        sale.total = totals["total"]

        db.commit()
        db.refresh(sale)
        return sale

    except ClientNotFoundError:
        raise HTTPException(404, "Client not found")

    except ProductNotFoundError as e:
        raise HTTPException(404, f"Product with ID {e.product_id} not found")

    except InsufficientStockError as e:
        raise HTTPException(
            400,
            f"Insufficient stock for product '{e.product_name}'. Available: {e.available}, Requested: {e.requested}"
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Database integrity error")

    except Exception:
        db.rollback()
        raise HTTPException(500, "Error creating sale")


@router.get("/", response_model=List[SaleResponse])
def list_sales(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all sales ordered by creation date (newest first)"""
    return list_sales_service(db)

@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a single sale by ID with all items"""
    try:
        return get_sale_service(db, sale_id)
    except SaleNotFoundError:
        raise HTTPException(404, "Sale not found")

@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(
    sale_id: int,
    sale_data: SaleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a sale.
    
    Business logic:
    - If items are provided, delete old items and create new ones
    - Restore stock from old items
    - Validate and decrement stock for new items
    - Recalculate all totals
    """
    # Get existing sale
    try:
        sale, items = update_sale_service(db, sale_id, sale_data)

        if items is not None:
            totals = calculate_sale_totals_service(items)
            sale.subtotal = totals["subtotal"]
            sale.tax = totals["tax"]
            sale.discount = totals["discount"]
            sale.total = totals["total"]

        db.commit()
        db.refresh(sale)
        return sale

    except SaleNotFoundError:
        raise HTTPException(404, "Sale not found")

    except ClientNotFoundError:
        raise HTTPException(404, "Client not found")

    except ProductNotFoundError as e:
        raise HTTPException(404, f"Product with ID {e.product_id} not found")

    except InsufficientStockError as e:
        raise HTTPException(400, f"Insufficient stock for product '{e.product_name}'")

    except Exception:
        db.rollback()
        raise HTTPException(500, "Error updating sale")


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a sale and restore stock.
    
    Business logic:
    - Restore stock for all items
    - Delete sale (items will cascade)
    """
    # Get existing sale
    try:
        delete_sale_service(db, sale_id)
        db.commit()
        return

    except SaleNotFoundError:
        raise HTTPException(404, "Sale not found")

    except Exception:
        db.rollback()
        raise HTTPException(500, "Error deleting sale")