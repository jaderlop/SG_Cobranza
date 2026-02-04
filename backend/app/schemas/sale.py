from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal


# ==================== SALE ITEM SCHEMAS ====================

class SaleItemCreate(BaseModel):
    """Schema for creating a sale item - only quantity and unit_price from frontend"""
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    unit_price: Decimal = Field(..., gt=0, description="Unit price must be greater than 0")


class SaleItemUpdate(BaseModel):
    """Schema for updating a sale item"""
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    unit_price: Decimal = Field(..., gt=0, description="Unit price must be greater than 0")


class SaleItemResponse(BaseModel):
    """Schema for sale item response - includes calculated subtotal"""
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    
    model_config = ConfigDict(from_attributes=True)


# ==================== SALE SCHEMAS ====================

class SaleCreate(BaseModel):
    """Schema for creating a sale - frontend sends this"""
    sale_number: Optional[str] = Field(None, max_length=50, description="Sale number (auto-generated if not provided)")
    client_id: int = Field(..., gt=0, description="Client ID")
    sale_date: date = Field(..., description="Sale date")
    due_date: Optional[date] = Field(None, description="Payment due date")
    status: Optional[str] = Field("pending", max_length=50, description="Sale status")
    payment_status: Optional[str] = Field("unpaid", max_length=50, description="Payment status")
    notes: Optional[str] = Field(None, description="Additional notes")
    items: List[SaleItemCreate] = Field(..., min_length=1, description="List of sale items (at least 1 required)")


class SaleUpdate(BaseModel):
    """Schema for updating a sale"""
    sale_number: Optional[str] = Field(None, max_length=50)
    client_id: Optional[int] = Field(None, gt=0)
    sale_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = Field(None, max_length=50)
    payment_status: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    items: Optional[List[SaleItemUpdate]] = Field(None, min_length=1, description="List of sale items")


class SaleResponse(BaseModel):
    """Schema for sale response - includes all calculated fields"""
    id: int
    sale_number: Optional[str]
    client_id: int
    user_id: int
    sale_date: date
    due_date: Optional[date]
    subtotal: Decimal
    tax: Decimal
    discount: Decimal
    total: Decimal
    status: str
    payment_status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[SaleItemResponse]
    
    model_config = ConfigDict(from_attributes=True)
