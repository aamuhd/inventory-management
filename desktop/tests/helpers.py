from sqlmodel import Session, SQLModel, create_engine


# Import ALL models so they are registered
import app.modules.inventory.models
from app.modules.inventory.models.product import *
from app.modules.inventory.models.stock_movement import *
from app.modules.inventory.models.product_variant import *
from app.modules.inventory.models.supplier import Supplier


def create_test_session() -> Session:
    engine = create_engine("sqlite:///:memory:")

    SQLModel.metadata.create_all(engine)

    return Session(engine)