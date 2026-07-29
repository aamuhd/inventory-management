from decimal import Decimal

import pytest

from app.modules.inventory.exceptions import (
    DuplicateSupplierReturnError,
    DuplicateSupplierReturnItemError,
    InvalidSupplierNameError,
    InvalidSupplierReturnStateError,
    SupplierAlreadyExistsError,
    SupplierNotFoundError,
    SupplierReturnItemNotFoundError,
    SupplierReturnNotFoundError,
)
from app.modules.inventory.repositories.supplier_repository import (
    SupplierRepository,
)
from app.modules.inventory.repositories.supplier_return_repository import (
    SupplierReturnRepository
)
from app.modules.inventory.repositories.supplier_return_item_repository import (
    SupplierReturnItemRepository
)
from app.modules.inventory.services.supplier_service import (
    SupplierService,
)

from app.modules.inventory.services.supplier_return_service import (
    SupplierReturnService
)

from app.modules.inventory.enums.supplier_return_status import SupplierReturnStatus
from app.modules.inventory.services.stock_movement_service import StockMovementService
from app.modules.inventory.repositories.product_variant_repository import ProductVariantRepository
from app.modules.inventory.repositories.stock_movement_repository import StockMovementRepository
from app.modules.inventory.repositories.product_repository import ProductRepository
from app.modules.inventory.services.product_service import ProductService
from app.modules.inventory.services.product_variant_service import ProductVariantService
from app.modules.inventory.repositories.purchase_order_item_repository import PurchaseOrderItemRepository
from app.modules.inventory.repositories.purchase_order_repository import PurchaseOrderRepository
from app.modules.inventory.services.purchase_order_service import PurchaseOrderService
from tests.helpers import create_test_session
from uuid import UUID

from datetime import date




def create_services():

    session = create_test_session()

    return_repo = SupplierReturnRepository(session)
    item_repo = SupplierReturnItemRepository(session)
    movement_repo = StockMovementRepository(session)
    variant_repo = ProductVariantRepository(session)

    product_repo = ProductRepository(session)
    variant_repo = ProductVariantRepository(session)

    product_service = ProductService(product_repo)
    variant_service = ProductVariantService(variant_repo, product_service)

    supplier_repo = SupplierRepository(session)
    supplier_service = SupplierService(supplier_repo)
    movement_service = StockMovementService(movement_repo, variant_repo)

    supplier_return_service = SupplierReturnService(return_repo, item_repo, movement_service)


    purchase_order_repository = PurchaseOrderRepository(session)

    purchase_order_item_repository = (
        PurchaseOrderItemRepository(session)
    )

    purchase_order_service = PurchaseOrderService(
        purchase_order_repository,
        purchase_order_item_repository,
        supplier_service,
        variant_service,
        movement_service,
    )

  
    return (
                supplier_service, 
                supplier_return_service,
                product_service,
                variant_service,
                purchase_order_service,
            )

def create_product(product_service: ProductService):
    return product_service.create(
        name="Swiss Lace",
        brand="Classic",
        description="Premium lace",
        category_id=None,
    )

#def create_variant():



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


def create_supplier_return(
    supplier_return_service,
    supplier,
    return_number="SR-001",
):

    return supplier_return_service.create(
        supplier_id=supplier.id,
        purchase_order_id=None,
        return_number=return_number,
        return_date=date.today(),
        notes="Supplier return",
    )

def create_variant(
        product_service,
        variant_service,
):
    product = create_product(product_service)
    return variant_service.create(
        product_id=product.id,
        length=5,
        stock_quantity=10,
        reorder_level=2,
        cost_price=Decimal("2500"),
        selling_price=Decimal("3000"),
    )


def test_create_supplier_return():

    (
        supplier_service,
        supplier_return_service,
        _,
        _,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    supplier_return = supplier_return_service.create(
        supplier.id,
        None,
        "SR-001",
        date.today(),
        "Damaged fabrics",
    )

    assert supplier_return.return_number == "SR-001"
    assert supplier_return.status == SupplierReturnStatus.DRAFT


def test_duplicate_supplier_return():

    (
        supplier_service,
        supplier_return_service,
        _,
        _,
        _,

    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    supplier_return_service.create(
        supplier.id,
        None,
        "SR-001",
        date.today(),
        None,
    )

    with pytest.raises(
        DuplicateSupplierReturnError,
    ):
        supplier_return_service.create(
            supplier.id,
            None,
            "SR-001",
            date.today(),
            None,
        )


def test_add_item():

    (
        supplier_service,
        supplier_return_service,
        product_service,
        variant_service,
        _
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    supplier_return = create_supplier_return(
        supplier_return_service,
        supplier,
        'SR-002'
    )

    item = supplier_return_service.add_item(
        supplier_return.id,
        variant.id,
        5,
        "Damaged lace",
    )

    assert item.quantity == 5


def test_duplicate_item():

    (
        supplier_service,
        supplier_return_service,
        product_service,
        variant_service,
        _
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    supplier_return = create_supplier_return(
        supplier_return_service,
        supplier,
    )

    supplier_return_service.add_item(
        supplier_return.id,
        variant.id,
        5,
        "Damaged",
    )

    with pytest.raises(
        DuplicateSupplierReturnItemError,
    ):
        supplier_return_service.add_item(
            supplier_return.id,
            variant.id,
            2,
            "Wrong color",
        )


def test_update_item():

    (
        supplier_service,
        supplier_return_service,
        product_service,
        variant_service,
        _
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    supplier_return = create_supplier_return(
        supplier_return_service,
        supplier,
    )

    item = supplier_return_service.add_item(
        supplier_return.id,
        variant.id,
        5,
        "Damaged",
    )

    item = supplier_return_service.update_item(
        item.id,
        8,
        "Wrong colour",
    )

    assert item.quantity == 8


def test_delete_item():

    (
        supplier_service,
        supplier_return_service,
        product_service,
        variant_service,
        _
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    supplier_return = create_supplier_return(
        supplier_return_service,
        supplier,
        'SR-003'
    )

    item = supplier_return_service.add_item(
        supplier_return.id,
        variant.id,
        5,
        "Damaged",
    )

    supplier_return_service.delete_item(
        item.id,
    )

    with pytest.raises(
        SupplierReturnItemNotFoundError,
    ):
        supplier_return_service.get_item(
            item.id,
        )


def test_submit_supplier_return():

    (
        supplier_service,
        supplier_return_service,
        product_service,
        variant_service,
        _
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )
    
    variant = create_variant(
        product_service,
        variant_service,
    )
    
    variant.stock_quantity = 20

    variant_service.update(
        variant.id,
        product_id=variant.product_id,
        length=variant.length,
        stock_quantity=20,
        reorder_level=variant.reorder_level,
        cost_price=variant.cost_price,
        selling_price=variant.selling_price,
        barcode=variant.barcode,
        sku=variant.sku,
    )

    supplier_return = create_supplier_return(
        supplier_return_service,
        supplier,
        'SR-003'
    )

    supplier_return_service.add_item(
        supplier_return.id,
        variant.id,
        5,
        "Damaged",
    )

    supplier_return = supplier_return_service.submit(
        supplier_return.id,
    )

    assert supplier_return.status == SupplierReturnStatus.SUBMITTED

    variant = variant_service.get_by_id(
        variant.id,
    )

    assert variant.stock_quantity == 15


def test_delete_supplier_return():

    (
        supplier_service,
        supplier_return_service,
        _,
        _,
        _
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    supplier_return = create_supplier_return(
        supplier_return_service,
        supplier,
        'SR-004'
    )

    supplier_return_service.delete(
        supplier_return.id,
    )

    with pytest.raises(
        SupplierReturnNotFoundError,
    ):
        supplier_return_service.get_by_id(
            supplier_return.id,
        )


def test_delete_submitted_supplier_return():

    (
        supplier_service,
        supplier_return_service,
        product_service,
        variant_service,
        _
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )
    product = create_product(product_service)
    variant = variant_service.create(
        product_id=product.id,
        length=5,
        stock_quantity=10,
        reorder_level=2,
        cost_price=Decimal("2500"),
        selling_price=Decimal("3000"),
    )

    variant.stock_quantity = 10

    variant_service.update(
        variant.id,
        product_id=variant.product_id,
        length=variant.length,
        stock_quantity=10,
        reorder_level=variant.reorder_level,
        cost_price=variant.cost_price,
        selling_price=variant.selling_price,
        barcode=variant.barcode,
        sku=variant.sku,
    )

    supplier_return = create_supplier_return(
        supplier_return_service,
        supplier,
        'SR-003'
    )

    supplier_return_service.add_item(
        supplier_return.id,
        variant.id,
        5,
        "Damaged",
    )

    supplier_return_service.submit(
        supplier_return.id,
    )

    with pytest.raises(
        InvalidSupplierReturnStateError,
    ):
        supplier_return_service.delete(
            supplier_return.id,
        )


def test_get_all_supplier_returns():

    (
        supplier_service,
        supplier_return_service,
        _,
        _,
        _
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    create_supplier_return(
        supplier_return_service,
        supplier,
        'SR-006'
    )

    create_supplier_return(
        supplier_return_service,
        supplier,
        'SR-007'
    )

    returns = supplier_return_service.get_all()

    assert len(returns) == 2


