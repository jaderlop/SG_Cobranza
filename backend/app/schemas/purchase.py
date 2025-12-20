from typing import List
from pydantic import BaseModel, conint
from decimal import Decimal
from datetime import datetime

# ---------- ITEMS ----------

class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: conint(gt=0)
    unit_cost: Decimal

# ---------- PURCHASE ----------

class PurchaseCreate(BaseModel):
    supplier_id: int
    items: List[PurchaseItemCreate]

# ---------- RESPONSE ----------

class PurchaseItemResponse(BaseModel):
    product_id: int
    quantity: int
    unit_cost: Decimal
    subtotal: Decimal

    class Config:
        orm_mode = True

class PurchaseResponse(BaseModel):
    id: int
    total_amount: Decimal
    supplier_id: int
    user_id: int
    created_at: datetime
    items: List[PurchaseItemResponse]

    class Config:
        orm_mode = True
