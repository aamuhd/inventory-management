import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox

from app.modules.inventory.repositories.supplier_repository import SupplierRepository
from app.modules.inventory.services.supplier_service import SupplierService
from app.modules.inventory.ui.supplier_window import SupplierWindow
from tests.helpers import create_test_session


@pytest.fixture
def supplier_window(qtbot, monkeypatch):

    session = create_test_session()

    repository = SupplierRepository(session)

    service = SupplierService(repository)

    window = SupplierWindow(service)

    qtbot.addWidget(window)

    # Prevent QMessageBox dialogs blocking tests
    monkeypatch.setattr(
        QMessageBox,
        "information",
        lambda *args, **kwargs: QMessageBox.StandardButton.Ok,
    )

    monkeypatch.setattr(
        QMessageBox,
        "warning",
        lambda *args, **kwargs: QMessageBox.StandardButton.Ok,
    )

    monkeypatch.setattr(
        QMessageBox,
        "question",
        lambda *args, **kwargs: QMessageBox.StandardButton.Yes,
    )

    return window

def test_create_supplier(
    supplier_window,
    qtbot,
):

    form = supplier_window.form

    form.name_input.setText("ABC Textiles")
    form.contact_person_input.setText("John")
    form.phone_input.setText("08012345678")
    form.email_input.setText("abc@gmail.com")
    form.address_input.setPlainText("Kano")
    form.notes_input.setPlainText("Main supplier")

    qtbot.mouseClick(
        form.save_button,
        Qt.MouseButton.LeftButton,
    )

    assert supplier_window.table.table.rowCount() == 1

    supplier = supplier_window.table.selected_supplier()

    assert supplier is None

def test_edit_supplier(
    supplier_window,
    qtbot,
):

    form = supplier_window.form

    form.name_input.setText("ABC")

    qtbot.mouseClick(
        form.save_button,
        Qt.MouseButton.LeftButton,
    )

    table = supplier_window.table.table

    table.selectRow(0)

    supplier_window.edit_selected(
        supplier_window.table.selected_supplier(),
    )

    form.phone_input.setText("09000000000")

    qtbot.mouseClick(
        form.save_button,
        Qt.MouseButton.LeftButton,
    )

    supplier = supplier_window.table.selected_supplier()

    assert supplier.phone == "09000000000"


def test_clear_form(
    supplier_window,
    qtbot,
):

    form = supplier_window.form

    form.name_input.setText("ABC")

    qtbot.mouseClick(
        form.clear_button,
        Qt.MouseButton.LeftButton,
    )

    assert form.name_input.text() == ""

    assert form.save_button.text() == "Save"


def test_delete_supplier(
    supplier_window,
    qtbot,
):

    form = supplier_window.form

    form.name_input.setText("ABC")

    qtbot.mouseClick(
        form.save_button,
        Qt.MouseButton.LeftButton,
    )

    supplier_window.table.table.selectRow(0)

    qtbot.mouseClick(
        supplier_window.delete_button,
        Qt.MouseButton.LeftButton,
    )

    assert supplier_window.table.table.rowCount() == 0


def test_duplicate_supplier(
    supplier_window,
    qtbot,
):

    form = supplier_window.form

    form.name_input.setText("ABC")

    qtbot.mouseClick(
        form.save_button,
        Qt.MouseButton.LeftButton,
    )

    form.name_input.setText("ABC")

    qtbot.mouseClick(
        form.save_button,
        Qt.MouseButton.LeftButton,
    )

    assert supplier_window.table.table.rowCount() == 1


