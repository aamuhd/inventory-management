from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship
from sqlalchemy.orm import Mapped

from app.core.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.modules.sales.models.sale_item import SaleItem
    from app.modules.sales.models.sales_return import SalesReturn


class SalesReturnItem(BaseModel, table=True):
    __tablename__ = "sales_return_items"

    sales_return_id: UUID = Field(
        foreign_key="sales_returns.id",
    )

    sale_item_id: UUID = Field(
        foreign_key="sale_items.id",
    )

    quantity: int = Field(gt=0)

    unit_price: Decimal = Field(
        decimal_places=2,
        max_digits=12,
    )

    sales_return: Mapped["SalesReturn"] = Relationship(
        back_populates="items",
    )

    sale_item: Mapped["SaleItem"] = Relationship(
        back_populates="return_items",
    )