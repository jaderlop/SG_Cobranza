from pydantic import BaseModel, computed_field
from typing import Optional
from decimal import Decimal
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    price: Decimal
    unit: str = "unit"


class ProductCreate(ProductBase):
    sku: Optional[str] = None
    cost: Optional[Decimal] = None
    stock_quantity: int = 0
    min_stock_level: int = 0
    max_stock_level: Optional[int] = None


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    cost: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    min_stock_level: Optional[int] = None
    max_stock_level: Optional[int] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    id: int
    sku: Optional[str]
    stock_quantity: int
    is_active: Optional[bool] = True
    price: float
    created_at: datetime

    class Config:
        from_attributes = True


class ProductWithStock(BaseModel):
    id: int
    name: str
    sku: str
    category: Optional[str] = None
    price: float
    stock_quantity: int
    stock_status: str
    min_stock_level: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True