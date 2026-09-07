from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel
if TYPE_CHECKING:
    from app.modules.authentication.models.user import User


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

    users: List["User"] = Relationship(
        back_populates="role",
    )