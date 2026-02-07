"""
Dashboard API Endpoints
Provides REST endpoints for dashboard KPIs, charts, and metrics
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services import dashboard_service
from app.schemas.dashboard import (
    KPIResponse,
    DailyAmount,
    SalesByStatus,
    TopProduct
)

router = APIRouter(tags=["Dashboard"])


@router.get(
    "/kpis",
    response_model=KPIResponse,
    summary="Get main dashboard KPIs",
    description="Returns all 11 main KPIs including sales, purchases, products, clients, and stock metrics"
)
def get_dashboard_kpis(db: Session = Depends(get_db)):
    """
    Get all main dashboard KPIs
    
    Returns:
        KPIResponse: Object with all 11 KPIs
    """
    return dashboard_service.get_kpis(db)


@router.get(
    "/sales-by-day",
    response_model=List[DailyAmount],
    summary="Get sales by day",
    description="Returns sales amounts grouped by day for the last N days (default: 30)"
)
def get_sales_by_day(
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """
    Get sales grouped by day
    
    Args:
        days: Number of days to look back (1-365, default: 30)
        
    Returns:
        List[DailyAmount]: List of daily sales amounts
    """
    return dashboard_service.get_sales_by_day(db, days=days)


@router.get(
    "/purchases-by-day",
    response_model=List[DailyAmount],
    summary="Get purchases by day",
    description="Returns purchases amounts grouped by day for the last N days (default: 30)"
)
def get_purchases_by_day(
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back"),
    db: Session = Depends(get_db)
):
    """
    Get purchases grouped by day
    
    Args:
        days: Number of days to look back (1-365, default: 30)
        
    Returns:
        List[DailyAmount]: List of daily purchases amounts
    """
    return dashboard_service.get_purchases_by_day(db, days=days)


@router.get(
    "/sales-by-status",
    response_model=List[SalesByStatus],
    summary="Get sales distribution by payment status",
    description="Returns sales count and total amount grouped by payment status"
)
def get_sales_by_status(db: Session = Depends(get_db)):
    """
    Get sales distribution by payment status
    
    Returns:
        List[SalesByStatus]: List of sales metrics grouped by status
    """
    return dashboard_service.get_sales_by_status(db)


@router.get(
    "/top-products",
    response_model=List[TopProduct],
    summary="Get top selling products",
    description="Returns top N products by quantity sold (default: 5)"
)
def get_top_products(
    limit: int = Query(default=5, ge=1, le=50, description="Number of top products to return"),
    db: Session = Depends(get_db)
):
    """
    Get top selling products
    
    Args:
        limit: Number of top products to return (1-50, default: 5)
        
    Returns:
        List[TopProduct]: List of top products with sales metrics
    """
    return dashboard_service.get_top_products(db, limit=limit)
