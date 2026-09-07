from PySide6.QtCore import QDate, Qt, Signal
from PySide6.QtWidgets import (
    QComboBox,
    QDateEdit,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPlainTextEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    QLabel,
)


class PurchaseOrderForm(QWidget):

    create_clicked = Signal()
    update_clicked = Signal()
    clear_clicked = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName(
            "purchaseOrderForm"
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred,
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        title = QLabel(
            "Purchase Order Information"
        )

        title.setObjectName(
            "purchaseOrderFormTitle"
        )

        # -----------------------------------------------------
        # Supplier
        # -----------------------------------------------------

        self.supplier_combo = QComboBox()

        self.supplier_combo.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Order Number
        # -----------------------------------------------------

        self.order_number_edit = QLineEdit()

        self.order_number_edit.setPlaceholderText(
            "Enter order number"
        )

        self.order_number_edit.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Order Date
        # -----------------------------------------------------

        self.order_date_edit = QDateEdit()

        self.order_date_edit.setCalendarPopup(
            True
        )

        self.order_date_edit.setDate(
            QDate.currentDate()
        )

        self.order_date_edit.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Notes
        # -----------------------------------------------------

        self.notes_edit = QPlainTextEdit()

        self.notes_edit.setPlaceholderText(
            "Enter notes"
        )

        self.notes_edit.setMinimumHeight(
            100
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        form_layout = QFormLayout()

        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        form_layout.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        form_layout.setHorizontalSpacing(
            12
        )

        form_layout.setVerticalSpacing(
            10
        )

        form_layout.addRow(
            "Supplier:",
            self.supplier_combo,
        )

        form_layout.addRow(
            "Order Number:",
            self.order_number_edit,
        )

        form_layout.addRow(
            "Order Date:",
            self.order_date_edit,
        )

        form_layout.addRow(
            "Notes:",
            self.notes_edit,
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.create_button = QPushButton(
            "Create"
        )

        self.update_button = QPushButton(
            "Update"
        )

        self.clear_button = QPushButton(
            "Clear"
        )

        self.create_button.setObjectName(
            "createButton"
        )

        self.update_button.setObjectName(
            "updateButton"
        )

        self.clear_button.setObjectName(
            "clearButton"
        )

        self.create_button.setMinimumHeight(
            35
        )

        self.update_button.setMinimumHeight(
            35
        )

        self.clear_button.setMinimumHeight(
            35
        )

        self.create_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.update_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.clear_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.update_button.setEnabled(
            False
        )

        button_layout = QHBoxLayout()

        button_layout.setSpacing(
            8
        )

        button_layout.addWidget(
            self.create_button
        )

        button_layout.addWidget(
            self.update_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        # -----------------------------------------------------
        # Main Layout
        # -----------------------------------------------------

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        layout.setSpacing(
            10
        )

        layout.addWidget(
            title
        )

        layout.addLayout(
            form_layout
        )

        layout.addLayout(
            button_layout
        )

        # -----------------------------------------------------
        # Signals
        # -----------------------------------------------------

        self.create_button.clicked.connect(
            self.create_clicked.emit
        )

        self.update_button.clicked.connect(
            self.update_clicked.emit
        )

        self.clear_button.clicked.connect(
            self.clear_clicked.emit
        )

    # =========================================================
    # MODES
    # =========================================================

    def set_edit_mode(
        self,
    ) -> None:

        self.create_button.setEnabled(
            False
        )

        self.update_button.setEnabled(
            True
        )

    def set_create_mode(
        self,
    ) -> None:

        self.create_button.setEnabled(
            True
        )

        self.update_button.setEnabled(
            False
        )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(
        self,
    ) -> None:

        self.supplier_combo.setCurrentIndex(
            -1
        )

        self.order_number_edit.clear()

        self.order_date_edit.setDate(
            QDate.currentDate()
        )

        self.notes_edit.clear()

        self.set_create_mode()

        self.supplier_combo.setFocus()