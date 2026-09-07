from datetime import date
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlmodel import Field, Relationship
from sqlalchemy.orm import Mapped

from app.core.database.models.base import BaseModel
from app.modules.inventory.enums.supplier_return_status import SupplierReturnStatus

if TYPE_CHECKING:
    from app.modules.inventory.models.supplier import Supplier
    from app.modules.inventory.models.purchase_order import PurchaseOrder
    from app.modules.inventory.models.supplier_return_item import SupplierReturnItem


class SupplierReturn(BaseModel, table=True):
    __tablename__ = "supplier_returns"

    supplier_id: UUID = Field(
        foreign_key="suppliers.id",
        nullable=False,
    )

    purchase_order_id: UUID | None = Field(
        default=None,
        foreign_key="purchase_orders.id",
    )

    return_number: str = Field(
        unique=True,
        index=True,
    )

    return_date: date

    status: SupplierReturnStatus = Field(
        default=SupplierReturnStatus.DRAFT,
    )

    notes: str | None = None

    supplier: Mapped["Supplier"] = Relationship(
        back_populates="returns"
    )

    purchase_order: Mapped["PurchaseOrder"] = Relationship(
        back_populates="returns"
    )

    items: Mapped[List["SupplierReturnItem"]] = Relationship(
        back_populates="supplier_return",
        cascade_delete=True
    )