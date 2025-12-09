from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric, func
from app.core.database import Base


class Product(Base):
    """Product/Service model"""
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    sku = Column(String(100), unique=True, index=True)
    description = Column(String)
    category = Column(String(100), index=True)
    price = Column(Numeric(15, 2), nullable=False)
    cost = Column(Numeric(15, 2))
    stock_quantity = Column(Integer, default=0)
    unit = Column(String(50), default='unit')
    min_stock_level = Column(Integer, default=0)
    max_stock_level = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
