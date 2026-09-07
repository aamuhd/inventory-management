from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlmodel import Field, Relationship
from sqlalchemy.orm import Mapped

from app.core.database.models.base import BaseModel
from app.modules.sales.enums.sale_status import SaleStatus


if TYPE_CHECKING:
    from app.modules.sales.models.customer import Customer
    from app.modules.sales.models.sale_item import SaleItem
    from app.modules.sales.models.sale_payment import SalePayment
    from app.modules.sales.models.sales_return import SalesReturn


class Sale(BaseModel, table=True):
    __tablename__ = "sales"

    customer_id: UUID | None = Field(
        default=None,
        foreign_key="customers.id",
    )

    invoice_number: str = Field(
        index=True,
        unique=True,
    )

    sale_date: date

    notes: str | None = None

    status: SaleStatus = Field(
        default=SaleStatus.DRAFT,
    )

    total_amount: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
        max_digits=12,
    )

    customer: Mapped["Customer"] = Relationship(
        back_populates="sales",
    )

    items: Mapped[List["SaleItem"]] = Relationship(
        back_populates="sale",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
        },
    )

    payments: Mapped[List["SalePayment"]] = Relationship(
        back_populates="sale",
    )

    returns: Mapped[List["SalesReturn"]] = Relationship(
        back_populates="sale",
    )
