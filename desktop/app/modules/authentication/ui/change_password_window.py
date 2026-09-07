from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QDialog,
    QMessageBox,
    QVBoxLayout,
)

from app.core.application.navigation import Navigation
from app.core.session.current_session import CurrentSession

from app.modules.authentication.exceptions import (
    InvalidPasswordError,
)

from app.modules.authentication.services.user_service import (
    UserService,
)

from .change_password_form import ChangePasswordForm


class ChangePasswordWindow(QDialog):

    def __init__(
        self,
        navigation: Navigation,
        current_session: CurrentSession,
        user_service: UserService,
    ) -> None:

        super().__init__()

        self._navigation = navigation
        self._current_session = current_session
        self._user_service = user_service

        # =====================================================
        # WINDOW
        # =====================================================

        self.setWindowTitle(
            "Change Password"
        )

        self.setObjectName(
            "changePasswordWindow"
        )

        self.resize(
            500,
            350,
        )

        self.setMinimumSize(
            450,
            320,
        )

        self.setModal(
            True
        )

        # =====================================================
        # FORM
        # =====================================================

        self.ui = ChangePasswordForm()

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

        self.ui.change_button.clicked.connect(
            self.change_password
        )

        self.ui.password_edit.returnPressed.connect(
            self.change_password
        )

        self.ui.confirm_password_edit.returnPressed.connect(
            self.change_password
        )

        self.ui.password_edit.setFocus()

    # =========================================================
    # CHANGE PASSWORD
    # =========================================================

    def change_password(
        self,
    ) -> None:

        user = self._current_session.user

        if user is None:

            QMessageBox.critical(
                self,
                "Change Password",
                "No authenticated user was found.",
            )

            return

        password = (
            self.ui.password_edit.text()
        )

        confirm_password = (
            self.ui.confirm_password_edit.text()
        )

        # -----------------------------------------------------
        # Validate password
        # -----------------------------------------------------

        if not password:

            QMessageBox.warning(
                self,
                "Change Password",
                "Please enter a new password.",
            )

            self.ui.password_edit.setFocus()

            return

        if not confirm_password:

            QMessageBox.warning(
                self,
                "Change Password",
                "Please confirm your new password.",
            )

            self.ui.confirm_password_edit.setFocus()

            return

        if password != confirm_password:

            QMessageBox.warning(
                self,
                "Change Password",
                "Passwords do not match.",
            )

            self.ui.confirm_password_edit.clear()
            self.ui.confirm_password_edit.setFocus()

            return

        # -----------------------------------------------------
        # Change password
        # -----------------------------------------------------

        try:

            updated_user = (
                self._user_service.change_password(
                    user.id,
                    password,
                )
            )

        except InvalidPasswordError as error:

            QMessageBox.warning(
                self,
                "Change Password",
                str(error),
            )

            return

        # -----------------------------------------------------
        # Update current session
        # -----------------------------------------------------

        self._current_session.login(
            updated_user
        )

        # =====================================================
        # PASSWORD CHANGED SUCCESSFULLY
        # =====================================================

        QMessageBox.information(
            self,
            "Password Changed",
            (
                "Your password has been changed successfully.\n\n"
                "You can now continue to the dashboard."
            ),
            QMessageBox.StandardButton.Ok,
        )

        # =====================================================
        # ACCEPT DIALOG
        # =====================================================

        self.accept()

    # =========================================================
    # CLOSE
    # =========================================================

    def closeEvent(
        self,
        event: QCloseEvent,
    ) -> None:

        user = self._current_session.user

        if (
            user is not None
            and user.must_change_password
        ):

            event.ignore()

            QMessageBox.warning(
                self,
                "Password Change Required",
                (
                    "You must change your password before "
                    "continuing."
                ),
            )

            return

        event.accept()
