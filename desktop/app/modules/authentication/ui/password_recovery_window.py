from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
    QVBoxLayout,
)

from app.core.application.navigation import Navigation

from app.modules.authentication.exceptions import (
    AuthenticationError,
    InvalidPasswordError,
)

from app.modules.authentication.services.password_recovery_service import (
    PasswordRecoveryService,
)

from .password_recovery_form import PasswordRecoveryForm


class PasswordRecoveryWindow(QDialog):

    def __init__(
        self,
        navigation: Navigation,
        password_recovery_service: PasswordRecoveryService,
    ) -> None:

        super().__init__()

        self._navigation = navigation

        self._password_recovery_service = (
            password_recovery_service
        )

        # =====================================================
        # WINDOW
        # =====================================================

        self.setWindowTitle(
            "Password Recovery"
        )

        self.setObjectName(
            "passwordRecoveryWindow"
        )

        self.resize(
            500,
            550,
        )

        self.setMinimumSize(
            450,
            500,
        )

        self.setModal(
            True
        )

        # =====================================================
        # FORM
        # =====================================================

        self.ui = PasswordRecoveryForm()

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        main_layout.addWidget(
            self.ui
        )

        # =====================================================
        # SIGNALS
        # =====================================================

        self.ui.reset_button.clicked.connect(
            self.reset_password
        )

        self.ui.username_edit.returnPressed.connect(
            self._focus_recovery_code
        )

        self.ui.recovery_code_edit.returnPressed.connect(
            self._focus_password
        )

        self.ui.password_edit.returnPressed.connect(
            self._focus_confirm_password
        )

        self.ui.confirm_password_edit.returnPressed.connect(
            self.reset_password
        )

        self.ui.username_edit.setFocus()

    # =========================================================
    # FOCUS
    # =========================================================

    def _focus_recovery_code(
        self,
    ) -> None:

        self.ui.recovery_code_edit.setFocus()

    def _focus_password(
        self,
    ) -> None:

        self.ui.password_edit.setFocus()

    def _focus_confirm_password(
        self,
    ) -> None:

        self.ui.confirm_password_edit.setFocus()

    # =========================================================
    # RESET PASSWORD
    # =========================================================

    def reset_password(
        self,
    ) -> None:

        username = (
            self.ui.username_edit
            .text()
            .strip()
        )

        recovery_code = (
            self.ui.recovery_code_edit
            .text()
            .strip()
            .upper()
        )

        password = (
            self.ui.password_edit
            .text()
        )

        confirm_password = (
            self.ui.confirm_password_edit
            .text()
        )

        # -----------------------------------------------------
        # USERNAME
        # -----------------------------------------------------

        if not username:

            QMessageBox.warning(
                self,
                "Password Recovery",
                "Please enter your username.",
            )

            self.ui.username_edit.setFocus()

            return

        # -----------------------------------------------------
        # RECOVERY CODE
        # -----------------------------------------------------

        if not recovery_code:

            QMessageBox.warning(
                self,
                "Password Recovery",
                "Please enter your recovery code.",
            )

            self.ui.recovery_code_edit.setFocus()

            return

        # -----------------------------------------------------
        # PASSWORD
        # -----------------------------------------------------

        if not password:

            QMessageBox.warning(
                self,
                "Password Recovery",
                "Please enter a new password.",
            )

            self.ui.password_edit.setFocus()

            return

        # -----------------------------------------------------
        # CONFIRM PASSWORD
        # -----------------------------------------------------

        if not confirm_password:

            QMessageBox.warning(
                self,
                "Password Recovery",
                "Please confirm your new password.",
            )

            self.ui.confirm_password_edit.setFocus()

            return

        # -----------------------------------------------------
        # PASSWORD MATCH
        # -----------------------------------------------------

        if password != confirm_password:

            QMessageBox.warning(
                self,
                "Password Recovery",
                "Passwords do not match.",
            )

            self.ui.confirm_password_edit.clear()

            self.ui.confirm_password_edit.setFocus()

            return

        # -----------------------------------------------------
        # RESET
        # -----------------------------------------------------

        try:

            self._password_recovery_service.reset_password(
                username=username,
                recovery_code=recovery_code,
                new_password=password,
            )

            QMessageBox.information(
                self,
                "Password Reset",
                "Your password has been reset successfully. "
                "You can now log in with your new password.",
            )

            self.accept()

        except InvalidPasswordError as exc:

            QMessageBox.warning(
                self,
                "Password Recovery",
                str(exc),
            )

            self.ui.password_edit.clear()
            self.ui.confirm_password_edit.clear()
            self.ui.password_edit.setFocus()

        except AuthenticationError as exc:

            QMessageBox.warning(
                self,
                "Password Recovery",
                str(exc),
            )

            self.ui.recovery_code_edit.clear()
            self.ui.recovery_code_edit.setFocus()