from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from decimal import Decimal


class ClientBase(BaseModel):
    """Base client schema"""
    name: str
    tax_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    payment_terms: Optional[str] = None
    credit_limit: Optional[Decimal] = None
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    """Schema for creating a client"""
    name: str
    tax_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    payment_terms: Optional[str] = None
    credit_limit: Optional[Decimal] = None
    notes: Optional[str] = None


class ClientUpdate(BaseModel):
    """Schema for updating a client"""
    name: Optional[str] = None
    tax_id: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    postal_code: Optional[str] = None
    payment_terms: Optional[str] = None
    credit_limit: Optional[Decimal] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None


class ClientResponse(ClientBase):
    """Schema for client response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
