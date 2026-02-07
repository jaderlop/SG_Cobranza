"""
Dashboard Service - Business logic for dashboard KPIs and charts
Handles all calculations, aggregations, and data transformations for dashboard endpoints
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from datetime import date, timedelta
from typing import List, Dict
from decimal import Decimal

from app.models.sale import Sale
from app.models.purchase import Purchase
from app.models.product import Product
from app.models.client import Client
from app.models.sale_item import SaleItem
from app.models.purchase_item import PurchaseItem


def get_kpis(db: Session) -> Dict:
    """
    Get all main KPIs for the dashboard
    
    Returns:
        dict: Dictionary with all 11 KPIs
    """
    today = date.today()
    first_day_of_month = date(today.year, today.month, 1)
    
    # Total sales count
    total_sales_count = db.query(func.count(Sale.id)).scalar() or 0
    
    # Total sales amount
    total_sales_amount = db.query(func.sum(Sale.total)).scalar() or Decimal(0)
    
    # Total purchases amount
    total_purchases_amount = db.query(func.sum(Purchase.total)).scalar() or Decimal(0)
    
    # Total products
    total_products = db.query(func.count(Product.id)).filter(Product.is_active == True).scalar() or 0
    
    # Total clients
    total_clients = db.query(func.count(Client.id)).filter(Client.is_active == True).scalar() or 0
    
    # Sales today
    sales_today = db.query(func.sum(Sale.total)).filter(
        Sale.sale_date == today
    ).scalar() or Decimal(0)
    
    # Sales this month
    sales_this_month = db.query(func.sum(Sale.total)).filter(
        Sale.sale_date >= first_day_of_month
    ).scalar() or Decimal(0)
    
    # Purchases this month
    purchases_this_month = db.query(func.sum(Purchase.total)).filter(
        Purchase.purchase_date >= first_day_of_month
    ).scalar() or Decimal(0)
    
    # Pending sales count (payment_status = 'unpaid')
    pending_sales_count = db.query(func.count(Sale.id)).filter(
        Sale.payment_status == 'unpaid'
    ).scalar() or 0
    
    # Paid sales count (payment_status = 'paid')
    paid_sales_count = db.query(func.count(Sale.id)).filter(
        Sale.payment_status == 'paid'
    ).scalar() or 0
    
    # Low stock products count (stock_quantity <= min_stock_level)
    low_stock_products_count = db.query(func.count(Product.id)).filter(
        and_(
            Product.is_active == True,
            Product.stock_quantity <= Product.min_stock_level
        )
    ).scalar() or 0
    
    # Convert Decimal to float for JSON serialization
    return {
        "total_sales_count": total_sales_count,
        "total_sales_amount": float(total_sales_amount),
        "total_purchases_amount": float(total_purchases_amount),
        "total_products": total_products,
        "total_clients": total_clients,
        "sales_today": float(sales_today),
        "sales_this_month": float(sales_this_month),
        "purchases_this_month": float(purchases_this_month),
        "pending_sales_count": pending_sales_count,
        "paid_sales_count": paid_sales_count,
        "low_stock_products_count": low_stock_products_count
    }


def get_sales_by_day(db: Session, days: int = 30) -> List[Dict]:
    """
    Get sales grouped by day for the last N days
    
    Args:
        db: Database session
        days: Number of days to look back (default: 30)
        
    Returns:
        List of dicts with date and total amount
    """
    start_date = date.today() - timedelta(days=days)
    
    results = db.query(
        Sale.sale_date.label("date"),
        func.sum(Sale.total).label("total")
    ).filter(
        Sale.sale_date >= start_date
    ).group_by(
        Sale.sale_date
    ).order_by(
        Sale.sale_date
    ).all()
    
    # Convert to list of dicts with proper types
    return [
        {
            "date": str(r.date),
            "total": float(r.total) if r.total is not None else 0.0
        }
        for r in results
    ]


def get_purchases_by_day(db: Session, days: int = 30) -> List[Dict]:
    """
    Get purchases grouped by day for the last N days
    
    Args:
        db: Database session
        days: Number of days to look back (default: 30)
        
    Returns:
        List of dicts with date and total amount
    """
    start_date = date.today() - timedelta(days=days)
    
    results = db.query(
        Purchase.purchase_date.label("date"),
        func.sum(Purchase.total).label("total")
    ).filter(
        Purchase.purchase_date >= start_date
    ).group_by(
        Purchase.purchase_date
    ).order_by(
        Purchase.purchase_date
    ).all()
    
    # Convert to list of dicts with proper types
    return [
        {
            "date": str(r.date),
            "total": float(r.total) if r.total is not None else 0.0
        }
        for r in results
    ]


def get_sales_by_status(db: Session) -> List[Dict]:
    """
    Get sales distribution by payment_status
    
    Returns:
        List of dicts with status, count, and total_amount
    """
    results = db.query(
        Sale.payment_status.label("status"),
        func.count(Sale.id).label("count"),
        func.sum(Sale.total).label("total_amount")
    ).group_by(
        Sale.payment_status
    ).all()
    
    # Convert to list of dicts with proper types
    return [
        {
            "status": r.status,
            "count": r.count,
            "total_amount": float(r.total_amount) if r.total_amount is not None else 0.0
        }
        for r in results
    ]


def get_top_products(db: Session, limit: int = 5) -> List[Dict]:
    """
    Get top N products by quantity sold
    
    Args:
        db: Database session
        limit: Number of top products to return (default: 5)
        
    Returns:
        List of dicts with product info and sales metrics
    """
    results = db.query(
        Product.id.label("product_id"),
        Product.name.label("product_name"),
        func.sum(SaleItem.quantity).label("total_quantity"),
        func.sum(SaleItem.subtotal).label("total_amount")
    ).join(
        SaleItem, SaleItem.product_id == Product.id
    ).group_by(
        Product.id, Product.name
    ).order_by(
        func.sum(SaleItem.quantity).desc()
    ).limit(limit).all()
    
    # Convert to list of dicts with proper types
    return [
        {
            "product_id": r.product_id,
            "product_name": r.product_name,
            "total_quantity": r.total_quantity,
            "total_amount": float(r.total_amount) if r.total_amount is not None else 0.0
        }
        for r in results
    ]
