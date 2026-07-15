from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QFormLayout,
    QLineEdit,
    QPushButton,
)


class LoginForm(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.login_button = QPushButton("Login")

        self.password_edit.setEchoMode(QLineEdit.EchoMode.Password)

        form_layout = QFormLayout()
        form_layout.addRow("Username", self.username_edit)
        form_layout.addRow("Password", self.password_edit)

        layout = QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addWidget(self.login_button)