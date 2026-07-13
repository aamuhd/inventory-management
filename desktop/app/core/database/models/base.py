from datetime import datetime, timezone
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    """
    Base class for all database models.
    """

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    is_active: bool = Field(
        default=True,
        nullable=False,
    )

    is_deleted: bool = Field(
        default=False,
        nullable=False,
    )