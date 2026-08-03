from PySide6.QtCore import QDate, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from datetime import date


class SaleForm(QWidget):

    create_clicked = Signal()
    update_clicked = Signal()
    clear_clicked = Signal()

    def __init__(self):
        super().__init__()

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):

        self.customer_combo = QComboBox()

        self.invoice_number_edit = QLineEdit()

        self.sale_date_edit = QDateEdit()
        self.sale_date_edit.setCalendarPopup(True)
        self.sale_date_edit.setDate(
           self._today()
        )

        self.notes_edit = QTextEdit()

        form_layout = QFormLayout()

        form_layout.addRow(
            "Customer",
            self.customer_combo,
        )

        form_layout.addRow(
            "Invoice Number",
            self.invoice_number_edit,
        )

        form_layout.addRow(
            "Sale Date",
            self.sale_date_edit,
        )

        form_layout.addRow(
            "Notes",
            self.notes_edit,
        )

        self.create_button = QPushButton(
            "Create",
        )

        self.update_button = QPushButton(
            "Update",
        )

        self.clear_button = QPushButton(
            "Clear",
        )

        self.update_button.setEnabled(False)

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.create_button,
        )

        button_layout.addWidget(
            self.update_button,
        )

        button_layout.addWidget(
            self.clear_button,
        )

        layout = QVBoxLayout(self)

        layout.addLayout(
            form_layout,
        )

        layout.addLayout(
            button_layout,
        )

    def _connect_signals(self):

        self.create_button.clicked.connect(
            self.create_clicked.emit,
        )

        self.update_button.clicked.connect(
            self.update_clicked.emit,
        )

        self.clear_button.clicked.connect(
            self.clear_clicked.emit,
        )

    def _today(self) -> QDate:
        today = date.today()

        return QDate(
            today.year,
            today.month,
            today.day,
        )

    def clear(self):

        self.customer_combo.setCurrentIndex(-1)

        self.invoice_number_edit.clear()

        self.notes_edit.clear()
        
        self.sale_date_edit.setDate(
           self._today()
        )

        self.create_button.setEnabled(True)
        self.update_button.setEnabled(False)
