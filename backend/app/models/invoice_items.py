from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    DateTime,
    ForeignKey,
    String,
    func
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer,ForeignKey("invoices.id", ondelete="CASCADE"),nullable=False,index=True)
    product_id = Column(Integer,ForeignKey("products.id", ondelete="SET NULL"),nullable=True,index=True)
    description = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(15, 2), nullable=False)
    subtotal = Column(Numeric(15, 2), nullable=False)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)

    # Relaciones
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")
