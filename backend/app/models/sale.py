from sqlalchemy import Column, Integer, DateTime, Numeric, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")