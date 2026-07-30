from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.core.database.models.base import BaseModel

from typing import Optional, List

if TYPE_CHECKING:
    from app.modules.inventory.models.category import Category
    from app.modules.inventory.models.product_variant import ProductVariant


class Product(BaseModel, table=True):
    __tablename__ = "products"

    name: str = Field(index=True)

    brand: str | None = None

    description: str | None = None

    category_id: int | None = Field(
        default=None,
        foreign_key="categories.id",
    )

    category: Optional["Category"] = Relationship(
        back_populates="products",
    )

    variants: List["ProductVariant"] = Relationship(
        back_populates="product",
    )