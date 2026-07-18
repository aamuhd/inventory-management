from datetime import datetime, timezone

from sqlmodel import SQLModel, Field


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)

    name: str = Field(
        index=True,
        unique=True,
        max_length=100,
    )

    description: str = Field(default="", max_length=255)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))