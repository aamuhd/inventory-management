
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel
from app.modules.inventory.enums.purchase_order_status import (
    PurchaseOrderStatus,
)

if TYPE_CHECKING:
    from app.modules.inventory.models.supplier import Supplier
    from app.modules.inventory.models.purchase_order_item import PurchaseOrderItem


class PurchaseOrder(BaseModel, table=True):
    __tablename__ = "purchase_orders"

    supplier_id: UUID = Field(
        foreign_key="suppliers.id",
        nullable=False,
        index=True,
    )

    order_number: str = Field(
        index=True,
        unique=True,
    )

    status: PurchaseOrderStatus = Field(
        default=PurchaseOrderStatus.DRAFT,
    )

    order_date: date

    expected_date: date | None = None

    received_date: date | None = None

    total_amount: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
        max_digits=12,
    )

    notes: str | None = None

    supplier: "Supplier" = Relationship(
        back_populates="purchase_orders"
    )

    items: List["PurchaseOrderItem"] = Relationship(
        back_populates="purchase_order",
        cascade_delete=True,
    )