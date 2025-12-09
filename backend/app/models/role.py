from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base


class Role(Base):
    """Role model for user authorization"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String)
    created_at = Column(DateTime, server_default=func.now())
