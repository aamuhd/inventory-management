from sqlmodel import Field

from app.core.database.models.base import BaseModel


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