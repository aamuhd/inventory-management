from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel
from app.modules.inventory.enums.movement_type import MovementType

if TYPE_CHECKING:
    from app.modules.inventory.models.product_variant import ProductVariant


class StockMovement(BaseModel, table=True):
    __tablename__ = "stock_movements"

    variant_id: UUID = Field(
        foreign_key="product_variants.id",
        nullable=False,
        index=True,
    )

    movement_type: MovementType = Field(
        nullable=False,
    )

    quantity: int = Field(
        nullable=False,
    )

    reference: str | None = None

    notes: str | None = None

    variant: "ProductVariant" = Relationship(
        back_populates="movements",
    )