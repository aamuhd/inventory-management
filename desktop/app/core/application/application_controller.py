from app.modules.authentication.services.authentication_service import AuthenticationService
from app.core.session.current_session import CurrentSession
from app.modules.authentication.ui.login_window import LoginWindow
from app.modules.dashboard.ui.dashboard_window import DashboardWindow


class ApplicationController:
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
        self._login_window = LoginWindow(
            controller=self,
            authentication_service=self._authentication_service,
            current_session=self._current_session,
        )

        self._login_window.show()

    def show_dashboard(self) -> None:
        self._dashboard_window = DashboardWindow(
            controller=self,
            current_session=self._current_session,
        )

        self._dashboard_window.show()