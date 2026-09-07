from sqlmodel import SQLModel

from app.core.database.manager import DatabaseManager

# Inventory
from app.modules.inventory.models.category import Category
from app.modules.inventory.models.product import Product
from app.modules.inventory.models.product_variant import ProductVariant
from app.modules.inventory.models.stock_movement import StockMovement
from app.modules.inventory.models.supplier import Supplier
from app.modules.inventory.models.purchase_order import PurchaseOrder
from app.modules.inventory.models.purchase_order_item import (
    PurchaseOrderItem,
)
from app.modules.inventory.models.supplier_return import SupplierReturn
from app.modules.inventory.models.supplier_return_item import (
    SupplierReturnItem,
)

# Sales
from app.modules.sales.models.sale import Sale
from app.modules.sales.models.sale_item import SaleItem
from app.modules.sales.models.customer import Customer
from app.modules.sales.models.sales_return import SalesReturn
from app.modules.sales.models.sales_return_item import SalesReturnItem

# Authentication
from app.modules.authentication.models.user import User
from app.modules.authentication.models.role import Role

# Settings
from app.modules.settings.models.settings import Settings

# Payments
from app.modules.sales.models.sale_payment import SalePayment


class DatabaseInitializer:
    """
    Creates all database tables.
    """

    def __init__(
        self,
        database: DatabaseManager,
    ) -> None:
        self._database = database

    def initialize(self) -> None:
        SQLModel.metadata.create_all(
            self._database.engine
        )