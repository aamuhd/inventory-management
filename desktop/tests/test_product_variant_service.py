from sqlmodel import Session, SQLModel, create_engine


from sqlmodel import SQLModel

from app.modules.inventory.repositories.product_repository import ProductRepository
from app.modules.inventory.repositories.product_variant_repository import ProductVariantRepository
from app.modules.inventory.services.product_service import ProductService
from app.modules.inventory.services.product_variant_service import ProductVariantService
#import app.modules.inventory.models

from tests.helpers import create_test_session



from app.modules.inventory.models.category import Category
from app.modules.inventory.models.product import Product
from app.modules.inventory.models.product_variant import ProductVariant



def create_services():
    
    session = create_test_session()


    product_repository = ProductRepository(session)
    product_service = ProductService(product_repository)

    variant_repository = ProductVariantRepository(session)
    variant_service = ProductVariantService(
        variant_repository,
        product_service,
    )

    return product_service, variant_service



def create_product(product_service: ProductService):
    return product_service.create(
        name="Swiss Lace",
        brand="Classic",
        description="Premium lace",
        category_id=None,
    )


from decimal import Decimal


def test_create_variant():

    product_service, variant_service = create_services()

    product = create_product(product_service)

    variant = variant_service.create(
        product_id=product.id,
        length=5,
        stock_quantity=10,
        reorder_level=2,
        cost_price=Decimal("2500"),
        selling_price=Decimal("3000"),
    )

    assert variant.product_id == product.id
    assert variant.length == 5
    assert variant.stock_quantity == 10
    assert variant.cost_price == Decimal("2500")
    assert variant.selling_price == Decimal("3000")


import pytest

from app.modules.inventory.exceptions import (
    InvalidLengthError,
    InvalidPriceError,
    InvalidStockQuantityError,
    ProductVariantAlreadyExistsError,
    ProductVariantNotFoundError,
)


def test_duplicate_variant():

    product_service, variant_service = create_services()

    product = create_product(product_service)

    variant_service.create(
        product.id,
        5,
        10,
        2,
        Decimal("2500"),
        Decimal("3000"),
    )

    with pytest.raises(
        ProductVariantAlreadyExistsError
    ):
        variant_service.create(
            product.id,
            5,
            5,
            2,
            Decimal("2500"),
            Decimal("3000"),
        )


def test_same_product_different_length():

    product_service, variant_service = create_services()

    product = create_product(product_service)

    variant_service.create(
        product.id,
        5,
        10,
        2,
        Decimal("2500"),
        Decimal("3000"),
    )

    variant = variant_service.create(
        product.id,
        10,
        8,
        2,
        Decimal("5000"),
        Decimal("6000"),
    )

    assert variant.length == 10


def test_update_variant():

    product_service, variant_service = create_services()

    product = create_product(product_service)

    variant = variant_service.create(
        product.id,
        5,
        10,
        2,
        Decimal("2500"),
        Decimal("3000"),
    )

    updated = variant_service.update(
        variant.id,
        product.id,
        5,
        20,
        5,
        Decimal("2600"),
        Decimal("3200"),
    )

    assert updated.stock_quantity == 20
    assert updated.reorder_level == 5
    assert updated.cost_price == Decimal("2600")

def test_delete_variant():

    product_service, variant_service = create_services()

    product = create_product(product_service)

    variant = variant_service.create(
        product.id,
        5,
        10,
        2,
        Decimal("2500"),
        Decimal("3000"),
    )

    variant_service.delete(
        variant.id,
    )

    with pytest.raises(
        ProductVariantNotFoundError,
    ):
        variant_service.get_by_id(
            variant.id,
        )


def test_invalid_length():

    product_service, variant_service = create_services()

    product = create_product(product_service)

    with pytest.raises(
        InvalidLengthError,
    ):
        variant_service.create(
            product.id,
            0,
            10,
            2,
            Decimal("2500"),
            Decimal("3000"),
        )


def test_negative_stock():

    product_service, variant_service = create_services()

    product = create_product(product_service)

    with pytest.raises(
        InvalidStockQuantityError,
    ):
        variant_service.create(
            product.id,
            5,
            -1,
            2,
            Decimal("2500"),
            Decimal("3000"),
        )


def test_negative_price():

    product_service, variant_service = create_services()

    product = create_product(product_service)

    with pytest.raises(
        InvalidPriceError,
    ):
        variant_service.create(
            product.id,
            5,
            10,
            2,
            Decimal("-1"),
            Decimal("3000"),
        )