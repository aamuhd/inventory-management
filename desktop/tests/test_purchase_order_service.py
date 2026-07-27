from datetime import date
from decimal import Decimal

import pytest

from app.modules.inventory.enums.purchase_order_status import (
    PurchaseOrderStatus,
)
from app.modules.inventory.exceptions import (
    InvalidPurchaseOrderStateError,
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
from tests.helpers import create_test_session


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
    purchase_order_item_repository = PurchaseOrderItemRepository(
        session,
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


def test_create_purchase_order():

    supplier_service, purchase_order_service = create_services()

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order = purchase_order_service.create(
        supplier_id=supplier.id,
        order_number="PO-001",
        order_date=date.today(),
    )

    assert purchase_order.supplier_id == supplier.id
    assert purchase_order.order_number == "PO-001"
    assert purchase_order.status == PurchaseOrderStatus.DRAFT
    assert purchase_order.total_amount == Decimal("0.00")


def test_get_purchase_order():

    supplier_service, purchase_order_service = create_services()

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

    supplier_service, purchase_order_service = create_services()

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

    supplier_service, purchase_order_service = create_services()

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


from uuid import uuid4


def test_purchase_order_not_found():

    _, purchase_order_service = create_services()

    with pytest.raises(
        PurchaseOrderNotFoundError,
    ):
        purchase_order_service.get_by_id(
            uuid4(),
        )


def test_delete_non_draft_purchase_order():

    supplier_service, purchase_order_service = create_services()

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