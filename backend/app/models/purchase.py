from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)  
    purchase_number = Column(String(50), nullable=False, unique=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id", ondelete="RESTRICT"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    purchase_date = Column(Date, nullable=False, index=True)
    due_date = Column(Date, nullable=True)
    subtotal = Column(Numeric(15, 2), nullable=False, server_default="0")
    tax = Column(Numeric(15, 2), nullable=False, server_default="0")
    discount = Column(Numeric(15, 2), nullable=True, server_default="0")
    total = Column(Numeric(15, 2), nullable=False, server_default="0")
    status = Column(String(50), server_default="pending", index=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)
    
    # Relaciones
    supplier = relationship("Supplier")
    user = relationship("User")
    items = relationship("PurchaseItem",back_populates="purchase",cascade="all, delete-orphan")
