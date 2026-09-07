from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel


if TYPE_CHECKING:
    from app.modules.authentication.models.role import Role


class User(BaseModel, table=True):
    """
    Represents an application user.
    """

    __tablename__ = "users"

    username: str = Field(
        index=True,
        unique=True,
        max_length=50,
    )

    full_name: str = Field(
        max_length=100,
    )

    email: str | None = Field(
        default=None,
        unique=True,
        max_length=255,
    )

    password_hash: str = Field()

    role_id: UUID = Field(
        foreign_key="roles.id",
        index=True,
    )

    must_change_password: bool = Field(
        default=False,
    )

    # =========================================================
    # PASSWORD RECOVERY
    # =========================================================

    recovery_code_hash: str | None = Field(
        default=None,
    )

    recovery_code_created_at: datetime | None = Field(
        default=None,
    )

    # =========================================================
    # RELATIONSHIP
    # =========================================================

    role: Optional["Role"] = Relationship(
        back_populates="users",
    )