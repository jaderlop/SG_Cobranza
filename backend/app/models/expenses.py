from sqlalchemy import (Column,Integer,String,Date,DateTime,Numeric,Boolean,ForeignKey,func)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="RESTRICT"),nullable=False,index=True)
    supplier_id = Column(Integer,ForeignKey("suppliers.id", ondelete="SET NULL"),nullable=True,index=True)
    expense_date = Column(Date, nullable=False, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    category = Column(String(100), index=True)
    description = Column(String)
    payment_method = Column(String(50))
    reference_number = Column(String(100))
    is_recurring = Column(Boolean,nullable=False,server_default="false")
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

    # Relaciones
    user = relationship("User")
    supplier = relationship("Supplier")
