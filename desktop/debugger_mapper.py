from __future__ import annotations

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel
from sqlalchemy.orm import configure_mappers

if TYPE_CHECKING:
    from __main__ import B


class A(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    bs: list[B] = Relationship(back_populates="a")


class B(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)

    a_id: int | None = Field(default=None, foreign_key="a.id")

    a: A = Relationship(back_populates="bs")


configure_mappers()

print("OK")