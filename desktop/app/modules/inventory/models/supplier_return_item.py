from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel

if TYPE_CHECKING:
    from app.modules.inventory.models.product_variant import ProductVariant
    from app.modules.inventory.models.supplier_return import SupplierReturn


class SupplierReturnItem(BaseModel, table=True):
    __tablename__ = "supplier_return_items"

    supplier_return_id: UUID = Field(
        foreign_key="supplier_returns.id",
        nullable=False,
    )

    variant_id: UUID = Field(
        foreign_key="product_variants.id",
        nullable=False,
    )

    quantity: int = Field(
        gt=0,
    )

    reason: str

    supplier_return: "SupplierReturn" = Relationship(
        back_populates="items",
    )

    variant: "ProductVariant" = Relationship(
        back_populates="supplier_return_items",
    )