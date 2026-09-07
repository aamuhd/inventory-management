from app.core.security.password_hasher import PasswordHasher
from app.modules.authentication.exceptions import (
    InactiveUserError,
    InvalidCredentialsError,
)
from app.modules.authentication.models.user import User
from app.modules.authentication.repositories.user_repository import UserRepository


class AuthenticationService:
    """Handles user authentication."""

    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
    ) -> None:
        self._user_repository = user_repository
        self._password_hasher = password_hasher

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> User:

        user = self._user_repository.get_by_username(username)

        if user is None:
            raise InvalidCredentialsError("Invalid username or password.")

        if not self._password_hasher.verify_password(
            password,
            user.password_hash,
        ):
            raise InvalidCredentialsError("Invalid username or password.")

        if not user.is_active:
            raise InactiveUserError("User account is inactive.")

        print(
            "AUTH DEBUG:",
            user.username,
            "must_change_password =",
            user.must_change_password,
        )

        return user