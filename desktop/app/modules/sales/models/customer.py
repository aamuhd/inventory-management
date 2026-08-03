from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel
if TYPE_CHECKING:
    from app.modules.sales.models.sale import Sale


class Customer(BaseModel, table=True):
    __tablename__ = "customers"

    name: str = Field(
        index=True,
        min_length=2,
        max_length=100,
    )

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    email: str | None = Field(
        default=None,
        max_length=255,
    )

    address: str | None = Field(
        default=None,
        max_length=255,
    )

    sales: list["Sale"] = Relationship(
        back_populates="customer",
    )