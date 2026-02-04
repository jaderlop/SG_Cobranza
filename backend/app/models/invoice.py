from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Numeric,
    Boolean,
    ForeignKey,
    CheckConstraint,
    func
)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(100), nullable=False, unique=True, index=True)
    invoice_type = Column(String(20), nullable=False)
    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="SET NULL"),
        nullable=True
    )
    supplier_id = Column(
        Integer,
        ForeignKey("suppliers.id", ondelete="SET NULL"),
        nullable=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False
    )
    invoice_date = Column(Date, nullable=False)
    due_date = Column(Date)
    subtotal = Column(Numeric(15, 2), nullable=False, default=0)
    tax = Column(Numeric(15, 2), nullable=False, default=0)
    discount = Column(Numeric(15, 2), default=0)
    total = Column(Numeric(15, 2), nullable=False, default=0)
    image_path = Column(String(500))
    ocr_processed = Column(Boolean, default=False)
    status = Column(String(50), default="draft")
    notes = Column(String)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column( DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relaciones
    client = relationship("Client")
    supplier = relationship("Supplier")
    user = relationship("User")
    items = relationship("InvoiceItem ", back_populates="invoice", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint(
            "invoice_type IN ('income', 'expense')",
            name="check_invoice_type"
        ),
        CheckConstraint(
            "(invoice_type = 'income' AND client_id IS NOT NULL) OR "
            "(invoice_type = 'expense' AND supplier_id IS NOT NULL)",
            name="check_invoice_party"
        ),
    )