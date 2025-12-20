from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductWithStock
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()


def get_stock_status(product: Product) -> str:
    """Determine stock status"""
    if product.stock_quantity == 0:
        return "Out of Stock"
    elif product.stock_quantity <= product.min_stock_level:
        return "Low Stock"
    else:
        return "OK"


@router.get("/", response_model=List[ProductWithStock])
def get_products(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)

    products = query.offset(skip).limit(limit).all()

    result = []
    for product in products:
        result.append(
            ProductWithStock(
                id=product.id,
                name=product.name,
                sku=product.sku,
                category=product.category,
                price=float(product.price),
                stock_quantity=product.stock_quantity,
                min_stock_level=product.min_stock_level,
                is_active=bool(product.is_active),
                stock_status=get_stock_status(product),
                created_at=product.created_at,
            )
        )

    return result


@router.get("/{product_id}", response_model=ProductWithStock)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(404, "Product not found")

    return ProductWithStock(
        id=product.id,
        name=product.name,
        sku=product.sku,
        category=product.category,
        price=float(product.price),
        stock_quantity=product.stock_quantity,
        min_stock_level=product.min_stock_level,
        is_active=bool(product.is_active),
        stock_status=get_stock_status(product),
        created_at=product.created_at,
    )



@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new product"""
    # Check if SKU already exists
    if product_data.sku:
        existing = db.query(Product).filter(Product.sku == product_data.sku).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Product with this SKU already exists"
            )
    
    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Update only provided fields
    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a product"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    return None
