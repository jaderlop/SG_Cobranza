# Import all models here for easy access and Alembic detection
from app.models.role import Role
from app.models.user import User
from app.models.client import Client
from app.models.supplier import Supplier
from app.models.product import Product

__all__ = [
    "Role",
    "User",
    "Client",
    "Supplier",
    "Product",
]
