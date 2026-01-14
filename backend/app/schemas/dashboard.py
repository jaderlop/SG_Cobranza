from pydantic import BaseModel
from typing import List

class KPIResponse(BaseModel):
    total_sales: float
    total_purchases: float
    profit: float


class DailyAmount(BaseModel):
    date: str
    total: float


class ProductRanking(BaseModel):
    product_id: int
    product_name: str
    quantity: int
