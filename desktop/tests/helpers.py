from sqlmodel import Session, SQLModel, create_engine


# =========================================================
# INVENTORY MODELS
# =========================================================

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


# =========================================================
# SALES MODELS
# =========================================================

from app.modules.sales.models.customer import Customer
from app.modules.sales.models.sale import Sale
from app.modules.sales.models.sale_item import SaleItem
from app.modules.sales.models.sales_return import SalesReturn
from app.modules.sales.models.sales_return_item import (
    SalesReturnItem,
)


# =========================================================
# AUTHENTICATION MODELS
# =========================================================

from app.modules.authentication.models.user import User
from app.modules.authentication.models.role import Role


# =========================================================
# SETTINGS MODELS
# =========================================================

from app.modules.settings.models.settings import Settings


def create_test_session() -> Session:
    """
    Create a fresh in-memory SQLite database session.

    All application models are imported above so that SQLModel
    registers every table and SQLAlchemy can resolve all
    relationship mappings before the tables are created.
    """

    engine = create_engine(
        "sqlite:///:memory:"
    )

    SQLModel.metadata.create_all(
        engine
    )

    return Session(engine)
