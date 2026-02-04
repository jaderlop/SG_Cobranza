from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, func, String, Date
from sqlalchemy.orm import relationship
from app.core.database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_number = Column(String(50), unique=True)
    client_id = Column(Integer, ForeignKey("clients.id", ondelete="RESTRICT"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    sale_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=True)
    subtotal = Column(Numeric(15,2), nullable=False, server_default="0")
    tax = Column(Numeric(15,2), nullable=False, server_default="0")
    discount = Column(Numeric(15,2), nullable=False, server_default="0")
    total = Column(Numeric(15,2), nullable=False, server_default="0")
    status = Column(String(50), server_default="pending")
    payment_status = Column(String(50), server_default="unpaid")
    notes = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    client = relationship("Client", backref="sales")
    user = relationship("User", backref="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    
