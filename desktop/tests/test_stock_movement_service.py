from decimal import Decimal

import pytest

from app.modules.inventory.enums.movement_type import MovementType
from app.modules.inventory.exceptions import (
    InsufficientStockError,
    InvalidMovementQuantityError,
    StockMovementNotFoundError,
)
from app.modules.inventory.repositories.product_repository import ProductRepository
from app.modules.inventory.repositories.product_variant_repository import (
    ProductVariantRepository,
)
from app.modules.inventory.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from app.modules.inventory.services.product_service import ProductService
from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)
from app.modules.inventory.services.stock_movement_service import (
    StockMovementService,
)
from tests.helpers import create_test_session


def create_services():

    session = create_test_session()

    product_repository = ProductRepository(session)
    product_service = ProductService(product_repository)

    variant_repository = ProductVariantRepository(session)
    variant_service = ProductVariantService(
        variant_repository,
        product_service,
    )

    movement_repository = StockMovementRepository(session)

    movement_service = StockMovementService(
        movement_repository,
        variant_repository,
    )

    return (
        product_service,
        variant_service,
        movement_service,
    )


def create_variant(
    product_service,
    variant_service,
):

    product = product_service.create(
        name="Swiss Lace",
        brand="Gucci",
        description="Luxury lace",
        category_id=None,
    )

    return variant_service.create(
        product_id=product.id,
        length=5,
        stock_quantity=20,
        reorder_level=5,
        cost_price=Decimal("2500"),
        selling_price=Decimal("3000"),
    )


def test_purchase_stock():

    _, variant_service, movement_service = create_services()

    variant = create_variant(
        _,
        variant_service,
    )

    movement = movement_service.purchase_stock(
        variant.id,
        10,
    )

    updated = variant_service.get_by_id(
        variant.id,
    )

    assert movement.movement_type == MovementType.PURCHASE
    assert movement.quantity == 10
    assert updated.stock_quantity == 30


def test_sell_stock():

    _, variant_service, movement_service = create_services()

    variant = create_variant(
        _,
        variant_service,
    )

    movement = movement_service.sell_stock(
        variant.id,
        8,
    )

    updated = variant_service.get_by_id(
        variant.id,
    )

    assert movement.movement_type == MovementType.SALE
    assert movement.quantity == -8
    assert updated.stock_quantity == 12


def test_sell_insufficient_stock():

    _, variant_service, movement_service = create_services()

    variant = create_variant(
        _,
        variant_service,
    )

    with pytest.raises(
        InsufficientStockError,
    ):
        movement_service.sell_stock(
            variant.id,
            100,
        )


def test_adjust_stock_positive():

    _, variant_service, movement_service = create_services()

    variant = create_variant(
        _,
        variant_service,
    )

    movement_service.adjust_stock(
        variant.id,
        5,
    )

    updated = variant_service.get_by_id(
        variant.id,
    )

    assert updated.stock_quantity == 25


def test_adjust_stock_negative():

    _, variant_service, movement_service = create_services()

    variant = create_variant(
        _,
        variant_service,
    )

    movement_service.adjust_stock(
        variant.id,
        -5,
    )

    updated = variant_service.get_by_id(
        variant.id,
    )

    assert updated.stock_quantity == 15


def test_damage_stock():

    _, variant_service, movement_service = create_services()

    variant = create_variant(
        _,
        variant_service,
    )

    movement = movement_service.damage_stock(
        variant.id,
        3,
    )

    updated = variant_service.get_by_id(
        variant.id,
    )

    assert movement.movement_type == MovementType.DAMAGED
    assert updated.stock_quantity == 17


def test_return_in():

    _, variant_service, movement_service = create_services()

    variant = create_variant(
        _,
        variant_service,
    )

    movement_service.return_in(
        variant.id,
        2,
    )

    updated = variant_service.get_by_id(
        variant.id,
    )

    assert updated.stock_quantity == 22


def test_invalid_quantity():

    _, variant_service, movement_service = create_services()

    variant = create_variant(
        _,
        variant_service,
    )

    with pytest.raises(
        InvalidMovementQuantityError,
    ):
        movement_service.purchase_stock(
            variant.id,
            0,
        )


def test_get_by_variant():

    _, variant_service, movement_service = create_services()

    variant = create_variant(
        _,
        variant_service,
    )

    movement_service.purchase_stock(
        variant.id,
        10,
    )

    movement_service.sell_stock(
        variant.id,
        2,
    )

    movement_service.damage_stock(
        variant.id,
        1,
    )

    history = movement_service.get_by_variant(
        variant.id,
    )

    assert len(history) == 3


def test_delete_movement():

    product_service, variant_service, movement_service = create_services()

    variant = create_variant(
        product_service,
        variant_service,
    )

    movement = movement_service.purchase_stock(
        variant.id,
        5,
    )

    movement_service.delete(
        movement.id,
    )

    with pytest.raises(
        StockMovementNotFoundError,
    ):
        movement_service.get_by_id(
            movement.id,
        )