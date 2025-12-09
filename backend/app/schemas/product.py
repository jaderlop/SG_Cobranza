from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ProductBase(BaseModel):
    """Base product schema"""
    name: str
    sku: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Decimal
    cost: Optional[Decimal] = None
    stock_quantity: int = 0
    unit: str = 'unit'
    min_stock_level: int = 0
    max_stock_level: Optional[int] = None


class ProductCreate(ProductBase):
    """Schema for creating a product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product"""
    name: Optional[str] = None
    sku: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    price: Optional[Decimal] = None
    cost: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    unit: Optional[str] = None
    min_stock_level: Optional[int] = None
    max_stock_level: Optional[int] = None
    is_active: Optional[bool] = None


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductWithStock(ProductResponse):
    """Product with stock status"""
    stock_status: str  # 'OK', 'Low Stock', 'Out of Stock'
