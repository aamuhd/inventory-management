from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlmodel import Field, Relationship
from sqlalchemy.orm import Mapped

from app.core.database.models.base import BaseModel
from app.modules.sales.enums.sales_return_status import (
    SalesReturnStatus,
)

if TYPE_CHECKING:
    from app.modules.sales.models.sale import Sale
    from app.modules.sales.models.sales_return_item import (
        SalesReturnItem,
    )


class SalesReturn(BaseModel, table=True):
    __tablename__ = "sales_returns"

    sale_id: UUID = Field(
        foreign_key="sales.id",
    )

    return_number: str = Field(
        unique=True,
        index=True,
    )

    return_date: date

    reason: str | None = None

    status: SalesReturnStatus = Field(
        default=SalesReturnStatus.DRAFT,
    )

    total_amount: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
        max_digits=12,
    )

    sale: Mapped["Sale"] = Relationship(
        back_populates="returns",
    )

    items: Mapped[List["SalesReturnItem"]] = Relationship(
        back_populates="sales_return",
    )