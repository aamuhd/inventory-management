from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship
from sqlalchemy.orm import Mapped

from app.core.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.modules.inventory.models.purchase_order import PurchaseOrder
    from app.modules.inventory.models.product_variant import ProductVariant


class PurchaseOrderItem(BaseModel, table=True):
    __tablename__ = "purchase_order_items"

    purchase_order_id: UUID = Field(
        foreign_key="purchase_orders.id",
        nullable=False,
        index=True,
        ondelete="CASCADE"
    )

    product_variant_id: UUID = Field(
        foreign_key="product_variants.id",
        nullable=False,
        index=True,
    )

    quantity: int = Field(
        gt=0,
        nullable=False,
    )

    received_quantity: int = Field(
        default=0,
        ge=0,
    )

    unit_cost: Decimal = Field(
        decimal_places=2,
        max_digits=12,
    )

    purchase_order: Mapped["PurchaseOrder"] = Relationship(
        back_populates="items"
    )

    product_variant: Mapped["ProductVariant"] = Relationship(
        back_populates="purchase_order_items"
    )