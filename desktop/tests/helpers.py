from sqlmodel import Session, SQLModel, create_engine


# Import ALL models so they are registered
import app.modules.inventory.models
from app.modules.inventory.models.product import Product
from app.modules.inventory.models.stock_movement import StockMovement
from app.modules.inventory.models.product_variant import ProductVariant
from app.modules.inventory.models.supplier import Supplier
from app.modules.inventory.models.purchase_order import PurchaseOrder
from app.modules.inventory.models.purchase_order_item import PurchaseOrderItem
from app.modules.inventory.models.supplier_return import SupplierReturn
from app.modules.inventory.models.supplier_return_item import SupplierReturnItem


def create_test_session() -> Session:
    engine = create_engine("sqlite:///:memory:")

    SQLModel.metadata.create_all(engine)

    return Session(engine)