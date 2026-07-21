from uuid import UUID

from app.modules.inventory.exceptions import (
    InvalidProductNameError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
)
from app.modules.inventory.models.product import Product
from app.modules.inventory.repositories.product_repository import (
    ProductRepository,
)


class ProductService:

    def __init__(
        self,
        product_repository: ProductRepository,
    ) -> None:
        self._repository = product_repository

    def create(
        self,
        name: str,
        brand: str | None,
        description: str | None,
        category_id: int | None,
    ) -> Product:

        name = name.strip()
        brand = brand.strip() if brand else None

        if not name:
            raise InvalidProductNameError(
                "Product name cannot be empty."
            )

        existing = self._repository.get_by_name_and_brand(
            name,
            brand,
        )

        if existing is not None:
            raise ProductAlreadyExistsError(
                f'"{name}" already exists.'
            )

        product = Product(
            name=name,
            brand=brand,
            description=description,
            category_id=category_id,
        )

        return self._repository.create(product)
    
    def get_by_id(
        self,
        product_id: UUID,
    ) -> Product:

        product = self._repository.get_by_id(product_id)

        if product is None:
            raise ProductNotFoundError(
                "Product not found."
            )

        return product
    
    def get_all(self) -> list[Product]:
        return self._repository.get_all()
    
    def update(
        self,
        product_id: UUID,
        name: str,
        brand: str | None,
        description: str | None,
        category_id: int | None,
    ) -> Product:

        product = self.get_by_id(product_id)

        name = name.strip()
        brand = brand.strip() if brand else None

        if not name:
            raise InvalidProductNameError(
                "Product name cannot be empty."
            )

        existing = self._repository.get_by_name_and_brand(
            name,
            brand,
        )

        if (
            existing is not None
            and existing.id != product.id
        ):
            brand_text = brand or "No Brand"

            raise ProductAlreadyExistsError(
                f'Product "{name}" ({brand_text}) already exists.'
            )

        product.name = name
        product.brand = brand
        product.description = description
        product.category_id = category_id

        return self._repository.update(product)
    
    def delete(
        self,
        product_id: UUID,
    ) -> None:

        product = self.get_by_id(product_id)

        self._repository.delete(product)