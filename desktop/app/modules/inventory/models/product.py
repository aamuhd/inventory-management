from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel
#from app.modules.inventory.models.category import Category
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.inventory.models.category import Category


class Product(BaseModel, table=True):
    __tablename__ = "products"

    name: str = Field(index=True)

    brand: str | None = None

    description: str | None = None

    category_id: int | None = Field(
        default=None,
        foreign_key="categories.id",
    )

    category: "Category" = Relationship(
        sa_relationship_kwargs={
            "back_populates": "products",
        }
    )