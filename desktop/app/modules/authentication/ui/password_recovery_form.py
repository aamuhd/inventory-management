from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PasswordRecoveryForm(QWidget):

    def __init__(
        self,
    ) -> None:

        super().__init__()

        self.setObjectName(
            "passwordRecoveryForm"
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            35,
            30,
            35,
            30,
        )

        main_layout.setSpacing(
            10
        )

        # =====================================================
        # TITLE
        # =====================================================

        self.title_label = QLabel(
            "Password Recovery"
        )

        self.title_label.setObjectName(
            "passwordRecoveryTitle"
        )

        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(
            self.title_label
        )

        # =====================================================
        # DESCRIPTION
        # =====================================================

        self.description_label = QLabel(
            "Enter your username and local recovery code "
            "to reset your password."
        )

        self.description_label.setObjectName(
            "passwordRecoveryDescription"
        )

        self.description_label.setWordWrap(
            True
        )

        self.description_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(
            self.description_label
        )

        main_layout.addSpacing(
            18
        )

        # =====================================================
        # USERNAME
        # =====================================================

        username_label = QLabel(
            "Username"
        )

        username_label.setObjectName(
            "passwordRecoveryFieldLabel"
        )

        main_layout.addWidget(
            username_label
        )

        self.username_edit = QLineEdit()

        self.username_edit.setObjectName(
            "passwordRecoveryUsernameEdit"
        )

        self.username_edit.setPlaceholderText(
            "Enter username"
        )

        self.username_edit.setMinimumHeight(
            42
        )

        main_layout.addWidget(
            self.username_edit
        )

        main_layout.addSpacing(
            6
        )

        # =====================================================
        # RECOVERY CODE
        # =====================================================

        recovery_code_label = QLabel(
            "Recovery Code"
        )

        recovery_code_label.setObjectName(
            "passwordRecoveryCodeLabel"
        )

        main_layout.addWidget(
            recovery_code_label
        )

        self.recovery_code_edit = QLineEdit()

        self.recovery_code_edit.setObjectName(
            "passwordRecoveryCodeEdit"
        )

        self.recovery_code_edit.setPlaceholderText(
            "XXXX-XXXX-XXXX"
        )

        self.recovery_code_edit.setMinimumHeight(
            42
        )

        main_layout.addWidget(
            self.recovery_code_edit
        )

        main_layout.addSpacing(
            6
        )

        # =====================================================
        # NEW PASSWORD
        # =====================================================

        password_label = QLabel(
            "New Password"
        )

        password_label.setObjectName(
            "passwordRecoveryPasswordLabel"
        )

        main_layout.addWidget(
            password_label
        )

        self.password_edit = QLineEdit()

        self.password_edit.setObjectName(
            "passwordRecoveryPasswordEdit"
        )

        self.password_edit.setPlaceholderText(
            "Enter new password"
        )

        self.password_edit.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.password_edit.setMinimumHeight(
            42
        )

        main_layout.addWidget(
            self.password_edit
        )

        main_layout.addSpacing(
            6
        )

        # =====================================================
        # CONFIRM PASSWORD
        # =====================================================

        confirm_password_label = QLabel(
            "Confirm New Password"
        )

        confirm_password_label.setObjectName(
            "passwordRecoveryConfirmPasswordLabel"
        )

        main_layout.addWidget(
            confirm_password_label
        )

        self.confirm_password_edit = QLineEdit()

        self.confirm_password_edit.setObjectName(
            "passwordRecoveryConfirmPasswordEdit"
        )

        self.confirm_password_edit.setPlaceholderText(
            "Confirm new password"
        )

        self.confirm_password_edit.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        self.confirm_password_edit.setMinimumHeight(
            42
        )

        main_layout.addWidget(
            self.confirm_password_edit
        )

        # =====================================================
        # RESET BUTTON
        # =====================================================

        main_layout.addSpacing(
            15
        )

        self.reset_button = QPushButton(
            "Reset Password"
        )

        self.reset_button.setObjectName(
            "passwordRecoveryResetButton"
        )

        self.reset_button.setMinimumHeight(
            44
        )

        self.reset_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        main_layout.addWidget(
            self.reset_button
        )

        main_layout.addStretch()