from app.modules.authentication.services.authentication_service import AuthenticationService
from app.core.session.current_session import CurrentSession
from app.modules.authentication.ui.login_window import LoginWindow
from app.modules.dashboard.ui.dashboard_window import DashboardWindow
from app.core.application.navigation import Navigation


class ApplicationController(Navigation):
    def __init__(
        self,
        authentication_service: AuthenticationService,
        current_session: CurrentSession,
    ) -> None:
        self._authentication_service = authentication_service
        self._current_session = current_session

        self._login_window = None
        self._dashboard_window = None

    def show_login(self) -> None:
        if self._dashboard_window:
            self._dashboard_window.close()

        self._login_window = LoginWindow(
            navigation=self,
            authentication_service=self._authentication_service,
            current_session=self._current_session,
        )

        self._login_window.show()

    def show_dashboard(self) -> None:
        if self._login_window:
            self._login_window.close()

        self._dashboard_window = DashboardWindow(
            navigation=self,
            current_session=self._current_session,
        )

        self._dashboard_window.show()