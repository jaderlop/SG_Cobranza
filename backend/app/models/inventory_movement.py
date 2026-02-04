from sqlalchemy import (Column,Integer,String,Date,DateTime,ForeignKey,CheckConstraint,func)
from sqlalchemy.orm import relationship
from app.core.database import Base


class InventoryMovement(Base):
    __tablename__ = "inventory_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer,ForeignKey("products.id", ondelete="CASCADE"),nullable=False,index=True)
    movement_type = Column(String(20),nullable=False)
    quantity = Column(Integer, nullable=False)
    movement_date = Column(Date, nullable=False, index=True)
    reference_type = Column(String(50))
    reference_id = Column(Integer)

    user_id = Column(Integer,ForeignKey("users.id", ondelete="RESTRICT"),nullable=False,index=True)
    notes = Column(String)
    created_at = Column(DateTime,server_default=func.now(),nullable=False)

    # Constraints
    __table_args__ = (
        CheckConstraint(
            "movement_type IN ('in', 'out', 'adjustment')",
            name="check_movement_type"
        ),
    )

    # Relaciones
    product = relationship("Product")
    user = relationship("User")
