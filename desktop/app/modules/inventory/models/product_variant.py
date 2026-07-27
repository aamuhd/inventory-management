from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.modules.inventory.models.product import Product
    from app.modules.inventory.models.stock_movement import StockMovement


class ProductVariant(BaseModel, table=True):
    __tablename__ = "product_variants"

    product_id: UUID = Field(
        foreign_key="products.id",
        index=True,
    )

    length: int = Field(gt=0)

    stock_quantity: int = Field(default=0, ge=0)

    reorder_level: int = Field(default=5, ge=0)

    cost_price: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
        max_digits=12,
    )

    selling_price: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
        max_digits=12,
    )

    barcode: str | None = Field(
        default=None,
        index=True,
    )

    sku: str | None = Field(
        default=None,
        index=True,
    )

    product: "Product" = Relationship(
        back_populates="variants",
    )

    movements: List["StockMovement"] = Relationship(
        back_populates="variant"
    )