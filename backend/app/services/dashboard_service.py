# FIX: PurchaseItem tiene unit_cost, NO unit_price
# SaleItem sí tiene unit_price
from sqlalchemy import func
from app.models import SaleItem, PurchaseItem, Sale, Purchase, Product

# KPIs principales
def get_kpis(db):
    total_sales = db.query(
        func.sum(SaleItem.subtotal)
    ).scalar() or 0

    total_purchases = db.query(
        func.sum(PurchaseItem.subtotal)
    ).scalar() or 0

    return {
        "total_sales": float(total_sales),
        "total_purchases": float(total_purchases),
        "profit": float(total_sales - total_purchases)
    }


# Ventas por día
def sales_by_day(db):
    results = db.query(
        func.date(Sale.created_at).label("date"),
        func.sum(Sale.total_amount).label("total")
    ).group_by(
        func.date(Sale.created_at)
    ).order_by(func.date(Sale.created_at)).all()
    
    return [{"date": str(r.date), "total": float(r.total)} for r in results]


# Compras por día
def purchases_by_day(db):
    results = db.query(
        func.date(Purchase.created_at).label("date"),
        func.sum(Purchase.total_amount).label("total")
    ).group_by(
        func.date(Purchase.created_at)
    ).order_by(func.date(Purchase.created_at)).all()
    
    return [{"date": str(r.date), "total": float(r.total)} for r in results]


# Productos más vendidos
def top_products(db, limit=5):
    results = db.query(
        Product.id.label("product_id"),
        Product.name.label("product_name"),
        func.sum(SaleItem.quantity).label("quantity")
    ).join(SaleItem, SaleItem.product_id == Product.id).group_by(
        Product.id, Product.name
    ).order_by(
        func.sum(SaleItem.quantity).desc()
    ).limit(limit).all()
    
    return [{"product_id": r.product_id, "product_name": r.product_name, "quantity": r.quantity} for r in results]
