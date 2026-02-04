from sqlalchemy import (Column,Integer,String,Date,DateTime,Numeric,ForeignKey,func)
from sqlalchemy.orm import relationship
from app.core.database import Base


class Income(Base):
    __tablename__ = "income"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer,ForeignKey("users.id", ondelete="RESTRICT"),nullable=False,index=True)
    client_id = Column(Integer,ForeignKey("clients.id", ondelete="SET NULL"),nullable=True,index=True)
    income_date = Column(Date, nullable=False, index=True)
    amount = Column(Numeric(15, 2), nullable=False)
    category = Column(String(100), index=True)
    description = Column(String)
    source = Column(String(255))
    payment_method = Column(String(50))
    reference_number = Column(String(100))
    created_at = Column(DateTime,server_default=func.now(),nullable=False)
    updated_at = Column(DateTime,server_default=func.now(),onupdate=func.now(),nullable=False)

    # Relaciones
    user = relationship("User")
    client = relationship("Client")
