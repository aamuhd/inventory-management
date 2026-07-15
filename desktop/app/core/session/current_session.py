from datetime import datetime
from typing import Optional

from app.modules.authentication.models.user import User


class CurrentSession:
    """Stores information about the currently logged-in user."""

    def __init__(self) -> None:
        self._user: Optional[User] = None
        self._login_time: Optional[datetime] = None

    @property
    def user(self) -> Optional[User]:
        return self._user

    @property
    def login_time(self) -> Optional[datetime]:
        return self._login_time

    @property
    def is_authenticated(self) -> bool:
        return self._user is not None

    def login(self, user: User) -> None:
        self._user = user
        self._login_time = datetime.now()

    def logout(self) -> None:
        self._user = None
        self._login_time = None