from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QWidget,
)


class SalesReturnForm(QWidget):

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        layout = QFormLayout(self)

        self.sale_combo = QComboBox()
        
        self.return_number_edit = QLineEdit()
        self.return_number_edit.setReadOnly(True)
        self.return_date_edit = QDateEdit()
        self.customer_edit = QLineEdit()
        self.customer_edit.setReadOnly(True)
        self.status_edit = QLineEdit()
        self.status_edit.setReadOnly(True)

        self.return_date_edit.setCalendarPopup(True)
        self.return_date_edit.setDate(
            QDate.currentDate(),
        )

        self.reason_edit = QTextEdit()

        layout.addRow(
            "Sale",
            self.sale_combo,
        )

        layout.addRow(
            "Customer",
            self.customer_edit,
        )

        layout.addRow(
            "Return Number",
            self.return_number_edit,
        )

        layout.addRow(
            "Status",
            self.status_edit,
        )

        layout.addRow(
            "Return Date",
            self.return_date_edit,
        )

        layout.addRow(
            "Reason",
            self.reason_edit,
        )

        button_layout = QHBoxLayout()

        self.create_button = QPushButton(
            "Create",
        )

        self.update_button = QPushButton(
            "Update",
        )

        self.update_button.setEnabled(False)

        self.clear_button = QPushButton(
            "Clear",
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

        layout.addRow(
            button_layout,
        )

    def clear(self):

        self.sale_combo.setCurrentIndex(-1)
        self.customer_edit.clear()
        self.return_number_edit.clear()
        self.return_date_edit.setDate(
            QDate.currentDate(),
        )
        self.status_edit.clear()
        self.reason_edit.clear()