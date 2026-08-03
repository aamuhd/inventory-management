from sqlmodel import SQLModel

from .manager import DatabaseManager
from app.modules.inventory.models.category import Category
from app.modules.sales.models.sale import Sale
from app.modules.sales.models.sale_item import SaleItem


class DatabaseInitializer:
    """
    Creates all database tables.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self._database = database

    def initialize(self) -> None:
        SQLModel.metadata.create_all(self._database.engine)