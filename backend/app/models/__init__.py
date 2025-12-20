# Import all models here for easy access and Alembic detection
from app.models.role import Role
from app.models.user import User
from app.models.client import Client
from app.models.supplier import Supplier
from app.models.product import Product
from app.models.sale import Sale
from app.models.sale_item import SaleItem
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem


__all__ = [
    "Role",
    "User",
    "Client",
    "Supplier",
    "Product",
    "Sale",
    "SaleItem",
    "Purchase",
    "PurchaseItem"
]
