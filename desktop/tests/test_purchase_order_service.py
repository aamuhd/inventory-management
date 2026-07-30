from datetime import date
from decimal import Decimal
from uuid import uuid4

import pytest

from tests.helpers import create_test_session

from app.modules.inventory.enums.purchase_order_status import (
    PurchaseOrderStatus,
)

from app.modules.inventory.exceptions import (
    DuplicatePurchaseOrderItemError,
    EmptyPurchaseOrderError,
    InvalidPurchaseOrderStateError,
    OverReceiveError,
    ProductVariantNotFoundError,
    PurchaseOrderItemNotFoundError,
    PurchaseOrderNotFoundError,
)

from app.modules.inventory.repositories.product_repository import (
    ProductRepository,
)
from app.modules.inventory.repositories.product_variant_repository import (
    ProductVariantRepository,
)
from app.modules.inventory.repositories.purchase_order_item_repository import (
    PurchaseOrderItemRepository,
)
from app.modules.inventory.repositories.purchase_order_repository import (
    PurchaseOrderRepository,
)
from app.modules.inventory.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from app.modules.inventory.repositories.supplier_repository import (
    SupplierRepository,
)

from app.modules.inventory.services.product_service import (
    ProductService,
)
from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)
from app.modules.inventory.services.purchase_order_service import (
    PurchaseOrderService,
)
from app.modules.inventory.services.stock_movement_service import (
    StockMovementService,
)
from app.modules.inventory.services.supplier_service import (
    SupplierService,
)


def create_services():

    session = create_test_session()

    supplier_repository = SupplierRepository(session)
    supplier_service = SupplierService(
        supplier_repository,
    )

    product_repository = ProductRepository(session)
    product_service = ProductService(
        product_repository,
    )

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
        product_service,
        variant_service,
        purchase_order_service,
    )


def create_supplier(
    supplier_service,
):

    return supplier_service.create(
        name="ABC Textiles",
        phone="08012345678",
        email="abc@test.com",
        address="Kano",
    )


def create_variant(
    product_service,
    variant_service,
):

    product = product_service.create(
        name="Swiss Lace",
        brand="Gucci",
        description="Luxury Lace",
        category_id=None,
    )

    return variant_service.create(
        product_id=product.id,
        length=5,
        stock_quantity=0,
        reorder_level=2,
        cost_price=Decimal("2500"),
        selling_price=Decimal("3000"),
    )


def test_create_purchase_order():

    supplier_service, _, _, purchase_order_service = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    assert purchase_order.supplier_id == supplier.id
    assert purchase_order.order_number == "PO-001"
    assert purchase_order.status == PurchaseOrderStatus.DRAFT
    assert purchase_order.total_amount == Decimal("0.00")


def test_get_purchase_order():

    supplier_service, _, _, purchase_order_service = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    result = purchase_order_service.get_by_id(
        purchase_order.id,
    )

    assert result.id == purchase_order.id


def test_get_all_purchase_orders():

    supplier_service, _, _, purchase_order_service = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    purchase_order_service.create(
        supplier.id,
        "PO-002",
        date.today(),
    )

    orders = purchase_order_service.get_all()

    assert len(orders) == 2


def test_delete_purchase_order():

    supplier_service, _, _, purchase_order_service = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    purchase_order_service.delete(
        purchase_order.id,
    )

    with pytest.raises(
        PurchaseOrderNotFoundError,
    ):
        purchase_order_service.get_by_id(
            purchase_order.id,
        )


def test_purchase_order_not_found():

    _, _, _, purchase_order_service = create_services()

    with pytest.raises(
        PurchaseOrderNotFoundError,
    ):
        purchase_order_service.get_by_id(
            uuid4(),
        )


def test_delete_non_draft_purchase_order():

    supplier_service, _, _, purchase_order_service = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    purchase_order.status = PurchaseOrderStatus.ORDERED

    with pytest.raises(
        InvalidPurchaseOrderStateError,
    ):
        purchase_order_service.delete(
            purchase_order.id,
        )


def test_add_purchase_order_item():

    (
        supplier_service,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    item = purchase_order_service.add_item(
        purchase_order.id,
        variant.id,
        quantity=10,
        unit_cost=Decimal("2500"),
    )

    assert item.product_variant_id == variant.id
    assert item.quantity == 10
    assert item.unit_cost == Decimal("2500")


def test_purchase_order_total_updates():

    (
        supplier_service,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    purchase_order_service.add_item(
        purchase_order.id,
        variant.id,
        quantity=5,
        unit_cost=Decimal("2000"),
    )

    purchase_order = purchase_order_service.get_by_id(
        purchase_order.id,
    )

    assert purchase_order.total_amount == Decimal("10000")


def test_duplicate_purchase_order_item():

    (
        supplier_service,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    purchase_order_service.add_item(
        purchase_order.id,
        variant.id,
        5,
        Decimal("2000"),
    )

    with pytest.raises(
        DuplicatePurchaseOrderItemError,
    ):
        purchase_order_service.add_item(
            purchase_order.id,
            variant.id,
            2,
            Decimal("2000"),
        )


def test_add_item_non_draft_order():

    (
        supplier_service,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    purchase_order.status = PurchaseOrderStatus.ORDERED

    with pytest.raises(
        InvalidPurchaseOrderStateError,
    ):
        purchase_order_service.add_item(
            purchase_order.id,
            variant.id,
            5,
            Decimal("2500"),
        )


def test_add_item_purchase_order_not_found():

    (
        _,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    variant = create_variant(
        product_service,
        variant_service,
    )

    with pytest.raises(
        PurchaseOrderNotFoundError,
    ):
        purchase_order_service.add_item(
            uuid4(),
            variant.id,
            5,
            Decimal("2500"),
        )


def test_add_item_variant_not_found():

    (
        supplier_service,
        _,
        _,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    with pytest.raises(
        ProductVariantNotFoundError,
    ):
        purchase_order_service.add_item(
            purchase_order.id,
            uuid4(),
            5,
            Decimal("2500"),
        )


def test_submit_purchase_order():

    (
        supplier_service,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    purchase_order_service.add_item(
        purchase_order.id,
        variant.id,
        10,
        Decimal("2500"),
    )

    purchase_order_service.submit(
        purchase_order.id,
    )

    purchase_order = purchase_order_service.get_by_id(
        purchase_order.id,
    )

    assert purchase_order.status == PurchaseOrderStatus.ORDERED


def test_submit_empty_purchase_order():

    supplier_service, _, _, purchase_order_service = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    with pytest.raises(
        EmptyPurchaseOrderError,
    ):
        purchase_order_service.submit(
            purchase_order.id,
        )


def test_submit_purchase_order_twice():

    (
        supplier_service,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    purchase_order_service.add_item(
        purchase_order.id,
        variant.id,
        5,
        Decimal("2500"),
    )

    purchase_order_service.submit(
        purchase_order.id,
    )

    with pytest.raises(
        InvalidPurchaseOrderStateError,
    ):
        purchase_order_service.submit(
            purchase_order.id,
        )


def create_submitted_purchase_order():

    (
        supplier_service,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    item = purchase_order_service.add_item(
        purchase_order.id,
        variant.id,
        quantity=10,
        unit_cost=Decimal("2500"),
    )

    purchase_order_service.submit(
        purchase_order.id,
    )

    return (
        purchase_order_service,
        variant_service,
        purchase_order,
        item,
        variant,
    )


def test_receive_purchase_order_item():

    (
        purchase_order_service,
        variant_service,
        purchase_order,
        item,
        variant,
    ) = create_submitted_purchase_order()

    purchase_order_service.receive_item(
        item.id,
        10,
    )

    updated_variant = variant_service.get_by_id(
        variant.id,
    )

    assert updated_variant.stock_quantity == 10


def test_partial_receive():

    (
        purchase_order_service,
        variant_service,
        purchase_order,
        item,
        variant,
    ) = create_submitted_purchase_order()

    purchase_order_service.receive_item(
        item.id,
        4,
    )

    updated_item = purchase_order_service.get_item(
        item.id,
    )

    assert updated_item.received_quantity == 4

    purchase_order = purchase_order_service.get_by_id(
        purchase_order.id,
    )

    assert purchase_order.status == PurchaseOrderStatus.PARTIALLY_RECEIVED


def test_complete_receive():

    (
        purchase_order_service,
        variant_service,
        purchase_order,
        item,
        variant,
    ) = create_submitted_purchase_order()

    purchase_order_service.receive_item(
        item.id,
        4,
    )

    purchase_order_service.receive_item(
        item.id,
        6,
    )

    purchase_order = purchase_order_service.get_by_id(
        purchase_order.id,
    )

    assert purchase_order.status == PurchaseOrderStatus.RECEIVED


def test_over_receive():

    (
        purchase_order_service,
        _,
        _,
        item,
        _,
    ) = create_submitted_purchase_order()

    with pytest.raises(
        OverReceiveError,
    ):
        purchase_order_service.receive_item(
            item.id,
            11,
        )


def test_receive_draft_purchase_order():

    (
        supplier_service,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant = create_variant(
        product_service,
        variant_service,
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    item = purchase_order_service.add_item(
        purchase_order.id,
        variant.id,
        10,
        Decimal("2500"),
    )

    with pytest.raises(
        InvalidPurchaseOrderStateError,
    ):
        purchase_order_service.receive_item(
            item.id,
            5,
        )


def test_receive_unknown_item():

    (
        purchase_order_service,
        _,
        _,
        _,
        _,
    ) = create_submitted_purchase_order()

    with pytest.raises(
        PurchaseOrderItemNotFoundError,
    ):
        purchase_order_service.receive_item(
            uuid4(),
            5,
        )


def test_receive_all_items():

    (
        supplier_service,
        product_service,
        variant_service,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    variant1 = create_variant(
        product_service,
        variant_service,
    )

    variant2 = variant_service.create(
        product_id=variant1.product_id,
        length=10,
        stock_quantity=0,
        reorder_level=5,
        cost_price=Decimal("2000"),
        selling_price=Decimal("2500"),
    )

    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    purchase_order_service.add_item(
        purchase_order.id,
        variant1.id,
        10,
        Decimal("2000"),
    )

    purchase_order_service.add_item(
        purchase_order.id,
        variant2.id,
        20,
        Decimal("2100"),
    )

    purchase_order_service.submit(
        purchase_order.id,
    )

    purchase_order_service.receive_all(
        purchase_order.id,
    )

    variant1 = variant_service.get_by_id(
        variant1.id,
    )

    variant2 = variant_service.get_by_id(
        variant2.id,
    )

    assert variant1.stock_quantity == 10
    assert variant2.stock_quantity == 20

    purchase_order = purchase_order_service.get_by_id(
        purchase_order.id,
    )

    assert purchase_order.status == PurchaseOrderStatus.RECEIVED


def test_receive_all_after_partial():

    (
        purchase_order_service,
        variant_service,
        purchase_order,
        item,
        variant,
    ) = create_submitted_purchase_order()

    purchase_order_service.receive_item(
        item.id,
        4,
    )

    purchase_order_service.receive_all(
        purchase_order.id,
    )

    variant = variant_service.get_by_id(
        variant.id,
    )

    assert variant.stock_quantity == 10

    item = purchase_order_service.get_item(
        item.id,
    )

    assert item.received_quantity == 10

    purchase_order = purchase_order_service.get_by_id(
        purchase_order.id,
    )

    assert purchase_order.status == PurchaseOrderStatus.RECEIVED


def test_get_purchase_orders_by_supplier():

    (
        supplier_service,
        _,
        _,
        purchase_order_service,
    ) = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    
    purchase_order = purchase_order_service.create(
        supplier.id,
        "PO-001",
        date.today(),
    )

    orders = purchase_order_service.get_by_supplier(
        supplier.id,
    )

    assert len(orders) == 1

    assert orders[0].supplier_id == supplier.id