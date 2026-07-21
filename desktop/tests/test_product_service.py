from sqlmodel import Session, SQLModel

from app.core.database.manager import DatabaseManager
from app.modules.inventory.repositories.product_repository import ProductRepository
from app.modules.inventory.services.product_service import ProductService

from tests.helpers import create_test_session


def create_service() -> ProductService:
    manager = DatabaseManager()

    #SQLModel.metadata.create_all(manager.engine)

    session = create_test_session()

    repository = ProductRepository(session)

    return ProductService(repository)


def test_create_product() -> None:
    service = create_service()

    product = service.create(
        name="Swiss Lace",
        brand="ABC",
        description="Luxury lace",
        category_id=None,
    )

    assert product.id is not None
    assert product.name == "Swiss Lace"
    assert product.brand == "ABC"


import pytest

from app.modules.inventory.exceptions import ProductAlreadyExistsError


def test_duplicate_product() -> None:
    service = create_service()

    service.create(
        name="Swiss Lace",
        brand="ABC",
        description="Luxury lace",
        category_id=None,
    )

    with pytest.raises(ProductAlreadyExistsError):
        service.create(
            name="Swiss Lace",
            brand="ABC",
            description="Another description",
            category_id=None,
        )


def test_same_name_different_brand() -> None:
    service = create_service()

    service.create(
        name="Swiss Lace",
        brand="ABC",
        description="",
        category_id=None,
    )

    product = service.create(
        name="Swiss Lace",
        brand="XYZ",
        description="",
        category_id=None,
    )

    assert product.brand == "XYZ"


def test_update_product() -> None:
    service = create_service()

    product = service.create(
        name="Swiss Lace",
        brand="ABC",
        description="Luxury lace",
        category_id=None,
    )

    updated = service.update(
        product.id,
        name="Premium Swiss Lace",
        brand="ABC",
        description="Updated description",
        category_id=None,
    )

    assert updated.name == "Premium Swiss Lace"
    assert updated.description == "Updated description"


import pytest

from app.modules.inventory.exceptions import ProductNotFoundError


def test_delete_product() -> None:
    service = create_service()

    product = service.create(
        name="Swiss Lace",
        brand="ABC",
        description="Luxury lace",
        category_id=None,
    )

    service.delete(product.id)

    with pytest.raises(ProductNotFoundError):
        service.get_by_id(product.id)


from app.modules.inventory.exceptions import InvalidProductNameError


def test_empty_name() -> None:
    service = create_service()

    with pytest.raises(InvalidProductNameError):
        service.create(
            name="   ",
            brand="ABC",
            description="Luxury lace",
            category_id=None,
        )