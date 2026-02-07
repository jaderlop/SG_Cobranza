"""
Dashboard schemas - Response models for dashboard endpoints
All numeric values are returned as float (converted from Decimal)
All dates are returned as ISO format strings
"""
from pydantic import BaseModel, Field
from typing import List, Optional


class KPIResponse(BaseModel):
    """Response model for main KPIs"""
    total_sales_count: int = Field(..., description="Total number of sales")
    total_sales_amount: float = Field(..., description="Total sales amount in currency")
    total_purchases_amount: float = Field(..., description="Total purchases amount in currency")
    total_products: int = Field(..., description="Total number of products")
    total_clients: int = Field(..., description="Total number of clients")
    sales_today: float = Field(..., description="Sales amount for today")
    sales_this_month: float = Field(..., description="Sales amount for current month")
    purchases_this_month: float = Field(..., description="Purchases amount for current month")
    pending_sales_count: int = Field(..., description="Number of sales with unpaid payment status")
    paid_sales_count: int = Field(..., description="Number of sales with paid payment status")
    low_stock_products_count: int = Field(..., description="Number of products with stock below minimum level")

    class Config:
        json_schema_extra = {
            "example": {
                "total_sales_count": 150,
                "total_sales_amount": 75000.50,
                "total_purchases_amount": 45000.25,
                "total_products": 85,
                "total_clients": 42,
                "sales_today": 1250.00,
                "sales_this_month": 18500.75,
                "purchases_this_month": 12300.00,
                "pending_sales_count": 12,
                "paid_sales_count": 138,
                "low_stock_products_count": 7
            }
        }


class DailyAmount(BaseModel):
    """Response model for daily sales/purchases amounts"""
    date: str = Field(..., description="Date in ISO format (YYYY-MM-DD)")
    total: float = Field(..., description="Total amount for that day")

    class Config:
        json_schema_extra = {
            "example": {
                "date": "2026-02-04",
                "total": 2500.50
            }
        }


class SalesByStatus(BaseModel):
    """Response model for sales grouped by payment status"""
    status: str = Field(..., description="Payment status (unpaid, paid, partial, etc.)")
    count: int = Field(..., description="Number of sales with this status")
    total_amount: float = Field(..., description="Total amount for sales with this status")

    class Config:
        json_schema_extra = {
            "example": {
                "status": "paid",
                "count": 120,
                "total_amount": 65000.75
            }
        }


class TopProduct(BaseModel):
    """Response model for top selling products"""
    product_id: int = Field(..., description="Product ID")
    product_name: str = Field(..., description="Product name")
    total_quantity: int = Field(..., description="Total quantity sold")
    total_amount: float = Field(..., description="Total sales amount for this product")

    class Config:
        json_schema_extra = {
            "example": {
                "product_id": 5,
                "product_name": "Premium Widget",
                "total_quantity": 250,
                "total_amount": 12500.00
            }
        }
