from sqlalchemy import Column, Integer, ForeignKey, Numeric, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class PurchaseItem(Base):
    __tablename__ = "purchase_items"

    id = Column(Integer, primary_key=True, index=True)

    purchase_id = Column(Integer,ForeignKey("purchases.id", ondelete="CASCADE"),nullable=False,index=True)
    product_id = Column(Integer,ForeignKey("products.id", ondelete="RESTRICT"),nullable=False,index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(15, 2), nullable=False)
    subtotal = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)

    # Relaciones
    purchase = relationship("Purchase", back_populates="items")
    product = relationship("Product")

