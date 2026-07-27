from sqlmodel import Field, Relationship

from typing import TYPE_CHECKING, List

from app.core.database.models.base import BaseModel



if TYPE_CHECKING:
    from app.modules.inventory.models.purchase_order import PurchaseOrder
    from app.modules.inventory.models.supplier_return import SupplierReturn


class Supplier(BaseModel, table=True):
    __tablename__ = "suppliers"

    name: str = Field(
        index=True,
        unique=True,
        max_length=150,
    )

    contact_person: str | None = Field(
        default=None,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        max_length=30,
    )

    email: str | None = Field(
        default=None,
        max_length=150,
    )

    address: str | None = Field(
        default=None,
        max_length=255,
    )

    notes: str | None = Field(
        default=None,
        max_length=500,
    )

    purchase_orders: List["PurchaseOrder"] = Relationship(
        back_populates="supplier"
    )

    returns: List["SupplierReturn"] = Relationship(
        back_populates="supplier"
    )