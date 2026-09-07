#from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from uuid import UUID

from sqlmodel import Field, Relationship
from sqlalchemy.orm import Mapped

from app.core.database.models.base import BaseModel


if TYPE_CHECKING:
    from app.modules.sales.models.sale import Sale


class SalePayment(BaseModel, table=True):
    __tablename__ = "sale_payments"

    sale_id: UUID = Field(
        foreign_key="sales.id",
        nullable=False,
        index=True,
    )

    amount: Decimal = Field(
        decimal_places=2,
        max_digits=12,
        gt=0,
    )

    payment_date: date

    payment_method: str = Field(
        default="Cash",
        max_length=50,
    )

    notes: str | None = None

    sale: Mapped["Sale"] = Relationship(
        back_populates="payments",
    )
