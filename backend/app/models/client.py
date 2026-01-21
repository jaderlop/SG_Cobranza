from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric, func
from app.core.database import Base


class Client(Base):
    """Client/Customer model"""
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    tax_id = Column(String(50), unique=True, index=True)
    email = Column(String(255), index=True)
    phone = Column(String(50))
    address = Column(String)
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    postal_code = Column(String(20))
    payment_terms = Column(String(100))
    credit_limit = Column(Numeric(15, 2))
    notes = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())

