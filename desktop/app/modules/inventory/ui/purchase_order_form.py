from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
    QWidget,
)


class PurchaseOrderForm(QWidget):

    create_clicked = Signal()
    update_clicked = Signal()
    clear_clicked = Signal()

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        form_layout = QFormLayout()

        self.supplier_combo = QComboBox()
        self.order_number_edit = QLineEdit()
        self.order_date_edit = QDateEdit()
        self.order_date_edit.setCalendarPopup(True)
        self.notes_edit = QPlainTextEdit()

        form_layout.addRow(
            "Supplier",
            self.supplier_combo,
        )
        form_layout.addRow(
            "Order Number",
            self.order_number_edit,
        )
        form_layout.addRow(
            "Order Date",
            self.order_date_edit,
        )
        form_layout.addRow(
            "Notes",
            self.notes_edit,
        )

        layout.addLayout(form_layout)

        button_layout = QHBoxLayout()

        self.create_button = QPushButton("Create")
        self.update_button = QPushButton("Update")
        self.clear_button = QPushButton("Clear")

        self.update_button.setEnabled(False)

        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.update_button)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        self.create_button.clicked.connect(
            self.create_clicked.emit,
        )

        self.update_button.clicked.connect(
            self.update_clicked.emit,
        )

        self.clear_button.clicked.connect(
            self.clear_clicked.emit,
        )

    def clear(self):

        self.supplier_combo.setCurrentIndex(-1)
        self.order_number_edit.clear()
        self.notes_edit.clear()
        self.update_button.setEnabled(False)
        self.create_button.setEnabled(True)