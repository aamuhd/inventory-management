from uuid import UUID

from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel

from .role import Role


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
    )

    role: Role | None = Relationship()