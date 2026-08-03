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

        self._build_ui()

    def _build_ui(self) -> None:

        self.name_input = QLineEdit()

        self.phone_input = QLineEdit()

        self.email_input = QLineEdit()

        self.address_input = QTextEdit()
        self.address_input.setFixedHeight(70)


        self.save_button = QPushButton("Save")

        self.clear_button = QPushButton("Clear")

        form_layout = QFormLayout()

        form_layout.addRow(
            "Name",
            self.name_input,
        )

        form_layout.addRow(
            "Phone",
            self.phone_input,
        )

        form_layout.addRow(
            "Email",
            self.email_input,
        )

        form_layout.addRow(
            "Address",
            self.address_input,
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.save_button,
        )

        button_layout.addWidget(
            self.clear_button,
        )

        layout = QVBoxLayout(self)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

    def customer_data(self):

        return (
            self.name_input.text(),
            self.phone_input.text(),
            self.email_input.text(),
            self.address_input.toPlainText(),
        )

    def set_customer(
        self,
        name,
        phone,
        email,
        address,
    ):

        self.name_input.setText(name)
        self.phone_input.setText(phone or "")
        self.email_input.setText(email or "")
        self.address_input.setPlainText(address or "")

    def clear(self):

        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()
        self.address_input.clear()

    def set_create_mode(self):

        self.save_button.setText("Save")

    def set_edit_mode(self):

        self.save_button.setText("Update")