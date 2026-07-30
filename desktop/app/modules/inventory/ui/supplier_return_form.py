from datetime import date
from typing import cast
from uuid import UUID

from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.models.supplier import Supplier
from app.modules.inventory.models.purchase_order import PurchaseOrder


class SupplierReturnForm(QWidget):

    create_clicked = Signal()
    update_clicked = Signal()
    clear_clicked = Signal()

    def __init__(self):

        super().__init__()

        self._build_ui()

        self._connect_signals()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.supplier_combo = QComboBox()

        self.purchase_order_combo = QComboBox()

        self.return_number_edit = QLineEdit()

        self.return_date_edit = QDateEdit()

        self.return_date_edit.setCalendarPopup(
            True,
        )

        self.return_date_edit.setDate(
            QDate.currentDate(),
        )

        self.notes_edit = QTextEdit()

        form_layout.addRow(
            QLabel("Supplier"),
            self.supplier_combo,
        )

        form_layout.addRow(
            QLabel("Purchase Order"),
            self.purchase_order_combo,
        )

        form_layout.addRow(
            QLabel("Return Number"),
            self.return_number_edit,
        )

        form_layout.addRow(
            QLabel("Return Date"),
            self.return_date_edit,
        )

        form_layout.addRow(
            QLabel("Notes"),
            self.notes_edit,
        )

        layout.addLayout(
            form_layout,
        )

        button_layout = QHBoxLayout()

        self.create_button = QPushButton(
            "Create",
        )

        self.update_button = QPushButton(
            "Update",
        )

        self.clear_button = QPushButton(
            "Clear",
        )

        self.update_button.setEnabled(
            False,
        )

        button_layout.addWidget(
            self.create_button,
        )

        button_layout.addWidget(
            self.update_button,
        )

        button_layout.addWidget(
            self.clear_button,
        )

        layout.addLayout(
            button_layout,
        )

    def _connect_signals(self):

        self.create_button.clicked.connect(
            self.create_clicked,
        )

        self.update_button.clicked.connect(
            self.update_clicked,
        )

        self.clear_button.clicked.connect(
            self.clear_clicked,
        )

    def load_suppliers(
        self,
        suppliers: list[Supplier],
    ):

        self.supplier_combo.clear()

        for supplier in suppliers:

            self.supplier_combo.addItem(
                supplier.name,
                supplier.id,
            )

    def load_purchase_orders(
        self,
        purchase_orders: list[PurchaseOrder],
    ):

        self.purchase_order_combo.clear()

        self.purchase_order_combo.addItem(
            "None",
            None,
        )

        for purchase_order in purchase_orders:

            self.purchase_order_combo.addItem(
                purchase_order.order_number,
                purchase_order.id,
            )

    def supplier_id(self) -> UUID:

        return self.supplier_combo.currentData()

    def purchase_order_id(self) -> UUID | None:

        return self.purchase_order_combo.currentData()

    def return_number(self) -> str:

        return self.return_number_edit.text().strip()

    def return_date(self) -> date:
        return cast(
            date,
            self.return_date_edit.date().toPython(),
        )

    def notes(self) -> str:

        return self.notes_edit.toPlainText().strip()

    def clear(self):

        self.supplier_combo.setCurrentIndex(0)

        self.purchase_order_combo.setCurrentIndex(0)

        self.return_number_edit.clear()

        self.return_date_edit.setDate(
            QDate.currentDate(),
        )

        self.notes_edit.clear()

        self.create_button.setEnabled(
            True,
        )

        self.update_button.setEnabled(
            False,
        )