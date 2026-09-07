from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class CustomerForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName(
            "customerForm"
        )

        self._build_ui()

    def _build_ui(self) -> None:

        # =====================================================
        # INPUTS
        # =====================================================

        self.name_input = QLineEdit()

        self.name_input.setObjectName(
            "customerNameInput"
        )

        self.name_input.setPlaceholderText(
            "Enter customer name"
        )

        self.phone_input = QLineEdit()

        self.phone_input.setObjectName(
            "customerPhoneInput"
        )

        self.phone_input.setPlaceholderText(
            "Enter phone number"
        )

        self.email_input = QLineEdit()

        self.email_input.setObjectName(
            "customerEmailInput"
        )

        self.email_input.setPlaceholderText(
            "Enter email address"
        )

        self.address_input = QTextEdit()

        self.address_input.setObjectName(
            "customerAddressInput"
        )

        self.address_input.setPlaceholderText(
            "Enter customer address"
        )

        self.address_input.setFixedHeight(
            90
        )

        # =====================================================
        # FORM
        # =====================================================

        form_layout = QFormLayout()

        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        form_layout.setVerticalSpacing(
            12
        )

        form_layout.addRow(
            "Name:",
            self.name_input,
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

        # =====================================================
        # BUTTONS
        # =====================================================

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.setObjectName(
            "customerSaveButton"
        )

        self.save_button.setMinimumHeight(
            38
        )

        self.clear_button = QPushButton(
            "Clear"
        )

        self.clear_button.setObjectName(
            "customerClearButton"
        )

        self.clear_button.setMinimumHeight(
            38
        )

        button_layout = QHBoxLayout()

        button_layout.setSpacing(
            8
        )

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

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
            12
        )

        layout.addLayout(
            form_layout
        )

        layout.addLayout(
            button_layout
        )

        layout.addStretch()

    # =========================================================
    # DATA
    # =========================================================

    def customer_data(self):

        return (
            self.name_input.text().strip(),
            self.phone_input.text().strip(),
            self.email_input.text().strip(),
            self.address_input
            .toPlainText()
            .strip(),
        )

    def set_customer(
        self,
        name,
        phone,
        email,
        address,
    ) -> None:

        self.name_input.setText(
            name
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

    def clear(self) -> None:

        self.name_input.clear()

        self.phone_input.clear()

        self.email_input.clear()

        self.address_input.clear()

        self.name_input.setFocus()

    # =========================================================
    # MODES
    # =========================================================

    def set_create_mode(self) -> None:

        self.save_button.setText(
            "Save"
        )

    def set_edit_mode(self) -> None:

        self.save_button.setText(
            "Update"
        )