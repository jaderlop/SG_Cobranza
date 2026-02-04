from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User

from app.schemas.product import (
    ProductCreate, 
    ProductUpdate, 
    ProductResponse, 
    ProductWithStock
)

from app.services.product_service import (
    get_products_service,
    get_product_by_id_service,
    create_new_product_service,
    update_product_service,
    delete_product_service
    
)

router = APIRouter()

## Get all products
@router.get("/", response_model=List[ProductWithStock])
async def get_stock_products(
    skip: int=0,
    limit: int=100,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_products_service(
        db,
        skip,
        limit,
        category
    )

## Get product with ID
@router.get("/{product_id}", response_model=ProductWithStock)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):

    product = get_product_by_id_service(db, product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found")

    return product


## Create new product
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = create_new_product_service(db, product_data)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product with this SKU already exists"
        )

    return product

## Update product
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a product"""
    product = update_product_service(
        db,
        product_id,
        product_data
    )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return product

## Delete product
@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a product"""
    product = delete_product_service(
        db,
        product_id
        )

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return product
