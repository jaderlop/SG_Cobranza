from sqlalchemy import Column, Integer, ForeignKey, DateTime, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(Integer, primary_key=True, index=True)
    total_amount = Column(Numeric(10, 2), nullable=False, default=0)

    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    supplier = relationship("Supplier")
    user = relationship("User")
    items = relationship(
        "PurchaseItem",
        back_populates="purchase",
        cascade="all, delete-orphan"
    )
