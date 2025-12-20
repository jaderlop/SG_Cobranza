
from sqlalchemy import Column, Integer, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from app.core.database import Base

class SaleItem(Base):
    __tablename__ = "sale_items"

    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(15, 2), nullable=False)
    subtotal = Column(Numeric(15, 2), nullable=False)

    # Relaciones
    sale = relationship("Sale", back_populates="items")
    product = relationship("Product")
