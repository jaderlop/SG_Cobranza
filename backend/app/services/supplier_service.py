from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.supplier import Supplier

def validate_supplier_exists_service(db: Session, supplier_id: int) -> bool:
    """Check if a supplier exists by ID"""
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    return supplier is not None