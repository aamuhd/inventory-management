from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class LoginForm(QWidget):

    def __init__(self) -> None:

        super().__init__()

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            40,
            30,
            40,
            30,
        )

        # =====================================================
        # Login Card
        # =====================================================

        card = QFrame()

        card.setObjectName(
            "loginCard"
        )

        card.setMinimumWidth(
            360
        )

        card.setMaximumWidth(
            420
        )

        card_layout = QVBoxLayout(card)

        card_layout.setContentsMargins(
            32,
            30,
            32,
            32,
        )

        card_layout.setSpacing(
            10
        )

        # =====================================================
        # Title
        # =====================================================

        title = QLabel(
            "Inventory Management System"
        )

        title.setObjectName(
            "loginTitle"
        )

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        card_layout.addWidget(
            title
        )

        # =====================================================
        # Subtitle
        # =====================================================

        subtitle = QLabel(
            "Sign in to continue"
        )

        subtitle.setObjectName(
            "loginSubtitle"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        card_layout.addWidget(
            subtitle
        )

        card_layout.addSpacing(
            18
        )

        # =====================================================
        # Username
        # =====================================================

        username_label = QLabel(
            "Username"
        )

        username_label.setObjectName(
            "loginFieldLabel"
        )

        card_layout.addWidget(
            username_label
        )

        self.username_edit = QLineEdit()

        self.username_edit.setObjectName(
            "usernameEdit"
        )

        self.username_edit.setPlaceholderText(
            "Enter username"
        )

        self.username_edit.setMinimumHeight(
            42
        )

        card_layout.addWidget(
            self.username_edit
        )

        card_layout.addSpacing(
            6
        )

        # =====================================================
        # Password
        # =====================================================

        password_label = QLabel(
            "Password"
        )

        password_label.setObjectName(
            "loginFieldLabel"
        )

        card_layout.addWidget(
            password_label
        )

        self.password_edit = QLineEdit()

        self.password_edit.setObjectName(
            "passwordEdit"
        )

        self.password_edit.setPlaceholderText(
            "Enter password"
        )

        self.password_edit.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.password_edit.setMinimumHeight(
            42
        )

        card_layout.addWidget(
            self.password_edit
        )

        # =====================================================
        # Login Button
        # =====================================================

        card_layout.addSpacing(
            18
        )

        self.login_button = QPushButton(
            "Login"
        )

        self.login_button.setObjectName(
            "loginButton"
        )

        self.login_button.setMinimumHeight(
            44
        )

        self.login_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        card_layout.addWidget(
            self.login_button
        )

        # =====================================================
        # FORGOT PASSWORD
        # =====================================================

        self.forgot_password_button = QPushButton(
            "Forgot Password?"
        )

        self.forgot_password_button.setObjectName(
            "forgotPasswordButton"
        )

        self.forgot_password_button.setFlat(
            True
        )

        self.forgot_password_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        card_layout.addWidget(
            self.forgot_password_button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )

        # =====================================================
        # Center Card
        # =====================================================

        main_layout.addStretch()

        main_layout.addWidget(
            card,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        main_layout.addStretch()