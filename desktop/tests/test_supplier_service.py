from app.modules.inventory.exceptions import (
    InvalidSupplierNameError,
    SupplierAlreadyExistsError,
    SupplierNotFoundError,
)
from app.modules.inventory.repositories.supplier_repository import (
    SupplierRepository,
)
from app.modules.inventory.services.supplier_service import (
    SupplierService,
)

from tests.helpers import create_test_session
from uuid import UUID


def create_service() -> SupplierService:

    session = create_test_session()

    repository = SupplierRepository(session)

    return SupplierService(repository)


def create_supplier(
    service: SupplierService,
):

    return service.create(
        name="ABC Textiles",
        contact_person="John Doe",
        phone="08012345678",
        email="abc@example.com",
        address="Kano",
        notes="Main supplier",
    )


def test_create_supplier():

    service = create_service()

    supplier = create_supplier(service)

    assert supplier.id is not None
    assert supplier.name == "ABC Textiles"
    assert supplier.contact_person == "John Doe"
    assert supplier.phone == "08012345678"
    assert supplier.email == "abc@example.com"
    assert supplier.address == "Kano"
    assert supplier.notes == "Main supplier"


def test_duplicate_supplier():

    service = create_service()

    create_supplier(service)

    try:

        create_supplier(service)

        assert False

    except SupplierAlreadyExistsError:

        assert True


def test_update_supplier():

    service = create_service()

    supplier = create_supplier(service)

    updated = service.update(
        supplier.id,
        name="XYZ Fabrics",
        contact_person="Jane Doe",
        phone="09000000000",
        email="xyz@example.com",
        address="Lagos",
        notes="Updated",
    )

    assert updated.name == "XYZ Fabrics"
    assert updated.contact_person == "Jane Doe"
    assert updated.phone == "09000000000"
    assert updated.email == "xyz@example.com"
    assert updated.address == "Lagos"
    assert updated.notes == "Updated"


def test_delete_supplier():

    service = create_service()

    supplier = create_supplier(service)

    service.delete(supplier.id)

    try:

        service.get_by_id(supplier.id)

        assert False

    except SupplierNotFoundError:

        assert True


def test_empty_name():

    service = create_service()

    try:

        service.create(
            name="   ",
        )

        assert False

    except InvalidSupplierNameError:

        assert True


def test_get_all_suppliers():

    service = create_service()

    create_supplier(service)

    service.create(
        name="Bella Fabrics",
        contact_person="Ali",
    )

    suppliers = service.get_all()

    assert len(suppliers) == 2

    names = {supplier.name for supplier in suppliers}

    assert names == {
        "ABC Textiles",
        "Bella Fabrics",
    }


def test_supplier_not_found():

    service = create_service()

    fake_id = UUID("00000000-0000-0000-0000-000000000000")

    try:

        service.get_by_id(fake_id)

        assert False

    except SupplierNotFoundError:

        assert True