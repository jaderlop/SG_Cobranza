from sqlalchemy.orm import Session
from typing import List, Optional


from app.models.product import Product
from app.schemas.product import ProductWithStock, ProductCreate, ProductUpdate


def get_stock_status(product: Product) -> dict:
    """
    Return stock quantity and human-readable status
    """
    if product.stock_quantity == 0:
        status = "Out of Stock"
    elif product.stock_quantity <= product.min_stock_level:
        status = "Low Stock"
    else:
        status = "OK"

    return {
        "quantity": product.stock_quantity,
        "status": status
    }


def get_products_service(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None
) -> List[ProductWithStock]:

    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)

    products = query.offset(skip).limit(limit).all()

    result = []

    for product in products:
        stock_info = get_stock_status(product)

        result.append(
            ProductWithStock(
                id=product.id,
                name=product.name,
                sku=product.sku,
                category=product.category,
                price=float(product.price),
                stock_quantity=stock_info["quantity"],
                stock_status=stock_info["status"],
                min_stock_level=product.min_stock_level,
                is_active=bool(product.is_active),
                created_at=product.created_at
            )
        )

    return result

## Get prodcuts by ID
def get_product_by_id_service(
    db: Session,
    product_id: int=0) -> Optional[ProductWithStock]:

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    
    stock_info = get_stock_status(product)


    return ProductWithStock(
        id=product.id,
        name=product.name,
        sku=product.sku,
        category=product.category,
        price=float(product.price),
        stock_quantity=stock_info["quantity"],
        stock_status=stock_info["status"],
        min_stock_level=product.min_stock_level,
        is_active=bool(product.is_active),
        created_at=product.created_at

    )

## Create new product
def create_new_product_service(db: Session, product_data: ProductCreate):
    if product_data.sku:
        existing = db.query(Product).filter(Product.sku == product_data.sku).first()
        if existing:
            return None

    product = Product(**product_data.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

## Update product
def update_product_service(
    db: Session,
    product_id: int,
    product_data: ProductUpdate
    ):

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    update_data = product_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)
    return product

## Delete product
def delete_product_service(
    db: Session,
    product_id: int
    ):

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None
    
    db.delete(product)
    db.commit()
    return product

