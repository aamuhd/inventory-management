from PySide6.QtWidgets import (
    QMainWindow,
    QMessageBox,
)

from app.core.session.current_session import CurrentSession
from app.modules.authentication.exceptions import AuthenticationError
from app.modules.authentication.services.authentication_service import (
    AuthenticationService,
)

from .login_form import LoginForm


class LoginWindow(QMainWindow):
    def __init__(
        self,
        authentication_service: AuthenticationService,
        current_session: CurrentSession,
    ) -> None:
        super().__init__()

        self._authentication_service = authentication_service
        self._current_session = current_session

        self.setWindowTitle("Login")
        self.resize(450, 300)

        self.ui = LoginForm()
        self.setCentralWidget(self.ui)

        self.ui.login_button.clicked.connect(self.login)
        self.ui.password_edit.returnPressed.connect(self.login)

    def login(self) -> None:
        username = self.ui.username_edit.text().strip()
        password = self.ui.password_edit.text()

        if not username:
            QMessageBox.warning(
                self,
                "Login",
                "Please enter your username.",
            )
            return

        if not password:
            QMessageBox.warning(
                self,
                "Login",
                "Please enter your password.",
            )
            return

        try:
            user = self._authentication_service.authenticate(
                username,
                password,
            )

            self._current_session.login(user)

            QMessageBox.information(
                self,
                "Success",
                f"Welcome {user.full_name}!",
            )

            # TODO:
            # Open Dashboard
            # self.dashboard = DashboardWindow(...)
            # self.dashboard.show()

            self.close()

        except AuthenticationError as exc:
            QMessageBox.warning(
                self,
                "Login Failed",
                str(exc),
            )