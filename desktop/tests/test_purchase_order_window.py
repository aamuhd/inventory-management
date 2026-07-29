from decimal import Decimal
from datetime import date

import pytest
from PySide6.QtCore import Qt

from app.core.database.manager import DatabaseManager
from app.modules.inventory.ui.purchase_order_window import PurchaseOrderWindow

from app.modules.inventory.repositories.product_repository import ProductRepository
from app.modules.inventory.repositories.product_variant_repository import ProductVariantRepository
from app.modules.inventory.repositories.purchase_order_repository import PurchaseOrderRepository
from app.modules.inventory.repositories.supplier_repository import SupplierRepository

from app.modules.inventory.services.product_service import ProductService
from app.modules.inventory.services.product_variant_service import ProductVariantService
from app.modules.inventory.services.purchase_order_service import PurchaseOrderService
from app.modules.inventory.services.supplier_service import SupplierService

from sqlmodel import Session


def create_window(qtbot):

    database_manager = DatabaseManager()

    session = Session(database_manager.engine)

    supplier_repository = SupplierRepository(session)
    product_repository = ProductRepository(session)
    variant_repository = ProductVariantRepository(session)
    purchase_order_repository = PurchaseOrderRepository(session)

    supplier_service = SupplierService(
        supplier_repository,
    )

    product_service = ProductService(
        product_repository,
    )

    variant_service = ProductVariantService(
        variant_repository,
        product_repository,
    )

    purchase_order_service = PurchaseOrderService(
        purchase_order_repository,
        supplier_repository,
        variant_repository,
    )

    window = PurchaseOrderWindow(
        purchase_order_service,
        supplier_service,
        variant_service,
    )

    qtbot.addWidget(window)

    window.show()

    return (
        window,
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
        address="Kano",
    )



def create_product(
    product_service,
):
    return product_service.create(
        name="Swiss Lace",
        description="Luxury lace",
        brand="Aso-Oke",
    )


def create_variant(
    product_service,
    variant_service,
):
    product = create_product(
        product_service,
    )

    return variant_service.create(
        product_id=product.id,
        length=5,
        stock_quantity=10,
        reorder_level=2,
        cost_price=Decimal("2500"),
        selling_price=Decimal("3000"),
    )


def create_purchase_order(
    purchase_order_service,
    supplier,
):

    return purchase_order_service.create(
        supplier_id=supplier.id,
        order_number="PO-001",
        order_date=date.today(),
        expected_date=None,
        notes="Purchase Order",
    )


def test_create_purchase_order(
    qtbot,
):

    (
        window,
        supplier_service,
        _,
        _,
        purchase_order_service,
    ) = create_window(
        qtbot,
    )

    supplier = create_supplier(
        supplier_service,
    )

    window.form.load_suppliers(
        supplier_service.get_all(),
    )

    index = window.form.supplier_combo.findData(
        supplier.id,
    )

    window.form.supplier_combo.setCurrentIndex(
        index,
    )

    window.form.order_number_edit.setText(
        "PO-001",
    )

    window.form.notes_edit.setPlainText(
        "First Order",
    )

    qtbot.mouseClick(
        window.form.create_button,
        Qt.MouseButton.LeftButton,
    )

    orders = purchase_order_service.get_all()

    assert len(orders) == 1

    assert orders[0].order_number == "PO-001"


def test_edit_purchase_order(qtbot):

    (
        window,
        supplier_service,
        _,
        _,
        purchase_order_service,
    ) = create_window(qtbot)

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order = create_purchase_order(
        purchase_order_service,
        supplier,
    )

    window._load_purchase_orders()

    window._purchase_order_selected(
        purchase_order,
    )

    window.form.notes_edit.setPlainText(
        "Updated notes",
    )

    qtbot.mouseClick(
        window.form.update_button,
        Qt.MouseButton.LeftButton,
    )

    purchase_order = purchase_order_service.get_by_id(
        purchase_order.id,
    )

    assert purchase_order.notes == "Updated notes"


def test_clear_form(qtbot):

    (
        window,
        supplier_service,
        _,
        _,
        _
    ) = create_window(qtbot)

    supplier = create_supplier(
        supplier_service,
    )

    window.form.load_suppliers(
        supplier_service.get_all(),
    )

    index = window.form.supplier_combo.findData(
        supplier.id,
    )

    window.form.supplier_combo.setCurrentIndex(
        index,
    )

    window.form.order_number_edit.setText(
        "PO-001",
    )

    window.form.notes_edit.setPlainText(
        "Purchase Order",
    )

    qtbot.mouseClick(
        window.form.clear_button,
        Qt.MouseButton.LeftButton,
    )

    assert window.form.order_number_edit.text() == ""

    assert (
        window.form.notes_edit.toPlainText()
        == ""
    )


def test_delete_purchase_order(qtbot):

    (
        window,
        supplier_service,
        _,
        _,
        purchase_order_service,
    ) = create_window(qtbot)

    supplier = create_supplier(
        supplier_service,
    )

    purchase_order = create_purchase_order(
        purchase_order_service,
        supplier,
    )

    window._load_purchase_orders()

    window._purchase_order_selected(
        purchase_order,
    )

    purchase_order_service.delete(
        purchase_order.id,
    )

    with pytest.raises(Exception):
        purchase_order_service.get_by_id(
            purchase_order.id,
        )