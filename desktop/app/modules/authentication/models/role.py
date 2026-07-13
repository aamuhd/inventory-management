from typing import Optional

from sqlmodel import Field

from desktop.app.core.database.models.base import BaseModel


class Role(BaseModel, table=True):
    """
    Represents a user role.
    """

    __tablename__ = "roles"

    name: str = Field(
        max_length=50,
        unique=True,
        index=True,
    )

    description: str | None = Field(
        default=None,
        max_length=255,
    )