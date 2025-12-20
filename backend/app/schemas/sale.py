# app/schemas/sale.py
from pydantic import BaseModel
from typing import List
from datetime import datetime

class SaleItemCreate(BaseModel):
    product_id: int
    quantity: int

# Crear venta
class SaleCreate(BaseModel):
    items: List[SaleItemCreate]


# Venta
class SaleItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    subtotal: float

class SaleResponse(BaseModel):
    id: int
    total_amount: float
    created_at: datetime
    items: List[SaleItemResponse]

    class Config:
        from_attributes = True


