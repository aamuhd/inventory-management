from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class SupplierForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName(
            "supplierForm"
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
            "Supplier Information"
        )

        title.setObjectName(
            "supplierFormTitle"
        )

        # -----------------------------------------------------
        # Inputs
        # -----------------------------------------------------

        self.name_input = QLineEdit()

        self.name_input.setPlaceholderText(
            "Enter supplier name"
        )

        self.name_input.setMinimumHeight(
            35
        )

        self.contact_person_input = QLineEdit()

        self.contact_person_input.setPlaceholderText(
            "Enter contact person"
        )

        self.contact_person_input.setMinimumHeight(
            35
        )

        self.phone_input = QLineEdit()

        self.phone_input.setPlaceholderText(
            "Enter phone number"
        )

        self.phone_input.setMinimumHeight(
            35
        )

        self.email_input = QLineEdit()

        self.email_input.setPlaceholderText(
            "Enter email"
        )

        self.email_input.setMinimumHeight(
            35
        )

        self.address_input = QTextEdit()

        self.address_input.setPlaceholderText(
            "Enter supplier address"
        )

        self.address_input.setMinimumHeight(
            70
        )

        self.notes_input = QTextEdit()

        self.notes_input.setPlaceholderText(
            "Enter notes"
        )

        self.notes_input.setMinimumHeight(
            70
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
            "Name:",
            self.name_input,
        )

        form_layout.addRow(
            "Contact Person:",
            self.contact_person_input,
        )

        form_layout.addRow(
            "Phone:",
            self.phone_input,
        )

        form_layout.addRow(
            "Email:",
            self.email_input,
        )

        form_layout.addRow(
            "Address:",
            self.address_input,
        )

        form_layout.addRow(
            "Notes:",
            self.notes_input,
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.save_button = QPushButton(
            "Save"
        )

        self.clear_button = QPushButton(
            "Clear"
        )

        self.save_button.setObjectName(
            "saveButton"
        )

        self.clear_button.setObjectName(
            "clearButton"
        )

        self.save_button.setMinimumHeight(
            35
        )

        self.clear_button.setMinimumHeight(
            35
        )

        self.save_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.clear_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        # -----------------------------------------------------
        # Main Layout
        # -----------------------------------------------------

        layout = QVBoxLayout(self)

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

    # =========================================================
    # DATA
    # =========================================================

    def supplier_data(
        self,
    ) -> tuple[
        str,
        str,
        str,
        str,
        str,
        str,
    ]:

        return (
            self.name_input.text(),
            self.contact_person_input.text(),
            self.phone_input.text(),
            self.email_input.text(),
            self.address_input.toPlainText(),
            self.notes_input.toPlainText(),
        )

    # =========================================================
    # EDIT MODE
    # =========================================================

    def set_supplier(
        self,
        name,
        contact_person,
        phone,
        email,
        address,
        notes,
    ) -> None:

        self.name_input.setText(
            name
        )

        self.contact_person_input.setText(
            contact_person or ""
        )

        self.phone_input.setText(
            phone or ""
        )

        self.email_input.setText(
            email or ""
        )

        self.address_input.setPlainText(
            address or ""
        )

        self.notes_input.setPlainText(
            notes or ""
        )

    def set_create_mode(
        self,
    ) -> None:

        self.save_button.setText(
            "Save"
        )

    def set_edit_mode(
        self,
    ) -> None:

        self.save_button.setText(
            "Update"
        )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(
        self,
    ) -> None:

        self.name_input.clear()

        self.contact_person_input.clear()

        self.phone_input.clear()

        self.email_input.clear()

        self.address_input.clear()

        self.notes_input.clear()

        self.name_input.setFocus()