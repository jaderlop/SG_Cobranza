from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime, date
from decimal import Decimal


# ==================== PURCHASE ITEM SCHEMAS ====================

class PurchaseItemCreate(BaseModel):
    """Schema for creating a purchase item - only quantity and unit_price from frontend"""
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    unit_price: Decimal = Field(..., gt=0, description="Unit price must be greater than 0")


class PurchaseItemUpdate(BaseModel):
    """Schema for updating a purchase item"""
    product_id: int = Field(..., gt=0, description="Product ID")
    quantity: int = Field(..., gt=0, description="Quantity must be greater than 0")
    unit_price: Decimal = Field(..., gt=0, description="Unit price must be greater than 0")


class PurchaseItemResponse(BaseModel):
    """Schema for purchase item response - includes calculated subtotal"""
    id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal
    
    model_config = ConfigDict(from_attributes=True)


# ==================== PURCHASE SCHEMAS ====================

class PurchaseCreate(BaseModel):
    """Schema for creating a purchase - frontend sends this"""
    purchase_number: Optional[str] = Field(None, max_length=50, description="Purchase number (auto-generated if not provided)")
    supplier_id: int = Field(..., gt=0, description="Supplier ID")
    purchase_date: date = Field(..., description="Purchase date")
    due_date: Optional[date] = Field(None, description="Payment due date")
    status: Optional[str] = Field("pending", max_length=50, description="Purchase status")
    notes: Optional[str] = Field(None, description="Additional notes")
    items: List[PurchaseItemCreate] = Field(..., min_length=1, description="List of purchase items (at least 1 required)")


class PurchaseUpdate(BaseModel):
    """Schema for updating a purchase"""
    purchase_number: Optional[str] = Field(None, max_length=50)
    supplier_id: Optional[int] = Field(None, gt=0)
    purchase_date: Optional[date] = None
    due_date: Optional[date] = None
    status: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    items: Optional[List[PurchaseItemUpdate]] = Field(None, min_length=1, description="List of purchase items")


class PurchaseResponse(BaseModel):
    """Schema for purchase response - includes all calculated fields"""
    id: int
    purchase_number: str
    supplier_id: int
    user_id: int
    purchase_date: date
    due_date: Optional[date]
    subtotal: Decimal
    tax: Decimal
    discount: Decimal
    total: Decimal
    status: str
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[PurchaseItemResponse]
    
    model_config = ConfigDict(from_attributes=True)
