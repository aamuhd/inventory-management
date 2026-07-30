from decimal import Decimal
from uuid import UUID

from app.modules.inventory.exceptions import (
    InvalidLengthError,
    InvalidPriceError,
    InvalidStockQuantityError,
    ProductVariantAlreadyExistsError,
    ProductVariantNotFoundError,
)
from app.modules.inventory.models.product_variant import ProductVariant
from app.modules.inventory.repositories.product_variant_repository import (
    ProductVariantRepository,
)
from app.modules.inventory.services.product_service import ProductService


class ProductVariantService:

    def __init__(
        self,
        variant_repository: ProductVariantRepository,
        product_service: ProductService,
    ) -> None:

        self._repository = variant_repository
        self._product_service = product_service

    def create(
        self,
        product_id: UUID,
        length: int,
        stock_quantity: int,
        reorder_level: int,
        cost_price: Decimal,
        selling_price: Decimal,
        barcode: str | None = None,
        sku: str | None = None,
    ) -> ProductVariant:

        # Ensure product exists
        self._product_service.get_by_id(product_id)

        if length <= 0:
            raise InvalidLengthError(
                "Length must be greater than zero."
            )

        if stock_quantity < 0:
            raise InvalidStockQuantityError(
                "Stock quantity cannot be negative."
            )

        if reorder_level < 0:
            raise InvalidStockQuantityError(
                "Reorder level cannot be negative."
            )

        if cost_price < 0:
            raise InvalidPriceError(
                "Cost price cannot be negative."
            )

        if selling_price < 0:
            raise InvalidPriceError(
                "Selling price cannot be negative."
            )

        existing = self._repository.get_by_product_and_length(
            product_id,
            length,
        )

        if existing is not None:
            raise ProductVariantAlreadyExistsError(
                f"A {length}-yard variant already exists."
            )

        variant = ProductVariant(
            product_id=product_id,
            length=length,
            stock_quantity=stock_quantity,
            reorder_level=reorder_level,
            cost_price=cost_price,
            selling_price=selling_price,
            barcode=barcode,
            sku=sku,
        )

        return self._repository.create(variant)

    def get_by_id(
        self,
        variant_id: UUID,
    ) -> ProductVariant:

        variant = self._repository.get_by_id(
            variant_id,
        )

        if variant is None:
            raise ProductVariantNotFoundError(
                "Product variant not found."
            )

        return variant

    def get_all(self) -> list[ProductVariant]:
        return self._repository.get_all()

    def get_by_product(
        self,
        product_id: UUID,
    ) -> list[ProductVariant]:

        return self._repository.get_by_product(
            product_id,
        )

    def update(
        self,
        variant_id: UUID,
        product_id: UUID,
        length: int,
        stock_quantity: int,
        reorder_level: int,
        cost_price: Decimal,
        selling_price: Decimal,
        barcode: str | None = None,
        sku: str | None = None,
    ) -> ProductVariant:

        variant = self.get_by_id(variant_id)

        self._product_service.get_by_id(product_id)

        if length <= 0:
            raise InvalidLengthError(
                "Length must be greater than zero."
            )

        if stock_quantity < 0:
            raise InvalidStockQuantityError(
                "Stock quantity cannot be negative."
            )

        if reorder_level < 0:
            raise InvalidStockQuantityError(
                "Reorder level cannot be negative."
            )

        if cost_price < 0:
            raise InvalidPriceError(
                "Cost price cannot be negative."
            )

        if selling_price < 0:
            raise InvalidPriceError(
                "Selling price cannot be negative."
            )

        existing = self._repository.get_by_product_and_length(
            product_id,
            length,
        )

        if (
            existing is not None
            and existing.id != variant.id
        ):
            raise ProductVariantAlreadyExistsError(
                f"A {length}-yard variant already exists."
            )

        variant.sqlmodel_update(
            {
                "product_id": product_id,
                "length": length,
                "stock_quantity": stock_quantity,
                "reorder_level": reorder_level,
                "cost_price": cost_price,
                "selling_price": selling_price,
                "barcode": barcode,
                "sku": sku,
            }
        )

        return self._repository.update(variant)

    def delete(
        self,
        variant_id: UUID,
    ) -> None:

        variant = self.get_by_id(
            variant_id,
        )

        self._repository.delete(variant)