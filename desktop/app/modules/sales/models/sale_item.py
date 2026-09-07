from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlmodel import Field, Relationship
from sqlalchemy.orm import Mapped

from app.core.database.models.base import BaseModel


if TYPE_CHECKING:
    from app.modules.sales.models.sale import Sale
    from app.modules.inventory.models.product_variant import ProductVariant
    from app.modules.sales.models.sales_return_item import SalesReturnItem


class SaleItem(BaseModel, table=True):
    __tablename__ = "sale_items"

    sale_id: UUID = Field(
        foreign_key="sales.id",
        nullable=False,
    )

    product_variant_id: UUID = Field(
        foreign_key="product_variants.id",
        nullable=False,
    )

    quantity: int = Field(
        gt=0,
    )

    unit_price: Decimal = Field(
        decimal_places=2,
        max_digits=12,
    )

    sale: Mapped["Sale"] = Relationship(
        back_populates="items",
    )

    product_variant: Mapped["ProductVariant"] = Relationship(
        back_populates="sale_items",
    )

    return_items: Mapped[List["SalesReturnItem"]] = Relationship(
        back_populates="sale_item",
    )