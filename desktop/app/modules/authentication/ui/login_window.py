from __future__ import annotations

from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from app.core.application.navigation import Navigation
from app.core.session.current_session import CurrentSession

from app.modules.authentication.exceptions import (
    AuthenticationError,
)

from app.modules.authentication.services.authentication_service import (
    AuthenticationService,
)

from .login_form import LoginForm


class LoginWindow(QMainWindow):

    def __init__(
        self,
        navigation: Navigation,
        authentication_service: AuthenticationService,
        current_session: CurrentSession,
    ) -> None:

        super().__init__()

        self._navigation = navigation

        self._authentication_service = (
            authentication_service
        )

        self._current_session = current_session

        # =====================================================
        # WINDOW
        # =====================================================

        self.setWindowTitle(
            "Login"
        )

        self.setObjectName(
            "loginWindow"
        )

        self.resize(
            500,
            500,
        )

        self.setMinimumSize(
            450,
            450,
        )

        # =====================================================
        # FORM
        # =====================================================

        self.ui = LoginForm()

        self.setCentralWidget(
            self.ui
        )

        # =====================================================
        # SIGNALS
        # =====================================================

        self.ui.login_button.clicked.connect(
            self.login
        )

        self.ui.forgot_password_button.clicked.connect(
            self._show_password_recovery
        )

        self.ui.password_edit.returnPressed.connect(
            self.login
        )

        self.ui.username_edit.returnPressed.connect(
            self.login
        )

        self.ui.username_edit.setFocus()

    # =========================================================
    # PASSWORD RECOVERY
    # =========================================================

    def _show_password_recovery(
        self,
    ) -> None:

        self._navigation.show_password_recovery()

    # =========================================================
    # LOGIN
    # =========================================================

    def login(self) -> None:

        username = (
            self.ui.username_edit
            .text()
            .strip()
        )

        password = (
            self.ui.password_edit
            .text()
        )

        # -----------------------------------------------------
        # Username validation
        # -----------------------------------------------------

        if not username:

            QMessageBox.warning(
                self,
                "Login",
                "Please enter your username.",
            )

            self.ui.username_edit.setFocus()

            return

        # -----------------------------------------------------
        # Password validation
        # -----------------------------------------------------

        if not password:

            QMessageBox.warning(
                self,
                "Login",
                "Please enter your password.",
            )

            self.ui.password_edit.setFocus()

            return

        # -----------------------------------------------------
        # Authentication
        # -----------------------------------------------------

        try:

            user = (
                self._authentication_service.authenticate(
                    username,
                    password,
                )
            )

            print(
                "DEBUG must_change_password:",
                user.must_change_password,
            )

            self._current_session.login(
                user
            )

            # =================================================
            # FIRST LOGIN
            # =================================================
            #
            # The user must change the temporary password
            # before entering the dashboard.
            #
            # Do NOT show the dashboard here.
            # ChangePasswordWindow is responsible for opening
            # the dashboard after the password is changed.
            #

            if user.must_change_password:

                self._navigation.show_change_password()

                return

            # =================================================
            # NORMAL LOGIN
            # =================================================

            QMessageBox.information(
                self,
                "Success",
                f"Welcome {user.full_name}!",
            )

            self.close()

            self._navigation.show_dashboard()

        except AuthenticationError as exc:

            QMessageBox.warning(
                self,
                "Login Failed",
                str(exc),
            )

            self.ui.password_edit.clear()

            self.ui.password_edit.setFocus()
