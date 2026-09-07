import re
import secrets
from uuid import UUID

from app.core.security.password_hasher import PasswordHasher

from app.modules.authentication.exceptions import (
    InvalidEmailError,
    InvalidFullNameError,
    InvalidPasswordError,
    InvalidRecoveryCodeError,
    InvalidUsernameError,
    RoleNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

from app.modules.authentication.models.user import User

from app.modules.authentication.repositories.role_repository import (
    RoleRepository,
)

from app.modules.authentication.repositories.user_repository import (
    UserRepository,
)


class UserService:

    # =========================================================
    # PASSWORD RECOVERY
    # =========================================================

    RECOVERY_CODE_LENGTH = 12

    RECOVERY_CODE_ALPHABET = (
        "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    )

    def __init__(
        self,
        user_repository: UserRepository,
        role_repository: RoleRepository,
        password_hasher: PasswordHasher,
    ) -> None:

        self._user_repository = user_repository
        self._role_repository = role_repository
        self._password_hasher = password_hasher

    # =========================================================
    # VALIDATION
    # =========================================================

    @staticmethod
    def _validate_email(
        email: str | None,
    ) -> str | None:

        if email is None:
            return None

        email = email.strip()

        if not email:
            return None

        pattern = (
            r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        )

        if not re.match(
            pattern,
            email,
        ):
            raise InvalidEmailError(
                "Invalid email address."
            )

        return email

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self,
        *,
        username: str,
        full_name: str,
        password: str,
        role_id: UUID,
        email: str | None = None,
    ) -> User:

        username = username.strip()
        full_name = full_name.strip()

        if not username:
            raise InvalidUsernameError(
                "Username cannot be empty."
            )

        if not full_name:
            raise InvalidFullNameError(
                "Full name cannot be empty."
            )

        if not password:
            raise InvalidPasswordError(
                "Password cannot be empty."
            )

        email = self._validate_email(
            email
        )

        existing = (
            self._user_repository.get_by_username(
                username
            )
        )

        if existing is not None:
            raise UserAlreadyExistsError(
                f'Username "{username}" already exists.'
            )

        if email is not None:

            existing = (
                self._user_repository.get_by_email(
                    email
                )
            )

            if existing is not None:
                raise UserAlreadyExistsError(
                    f'Email "{email}" already exists.'
                )

        role = self._role_repository.get_by_id(
            role_id
        )

        if role is None:
            raise RoleNotFoundError(
                "Role not found."
            )

        password_hash = (
            self._password_hasher.hash_password(
                password
            )
        )

        user = User(
            username=username,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role_id=role.id,
            must_change_password=True,
        )

        return self._user_repository.create(
            user
        )

    # =========================================================
    # GET
    # =========================================================

    def get_by_id(
        self,
        user_id: UUID,
    ) -> User:

        user = self._user_repository.get_by_id(
            user_id
        )

        if user is None:
            raise UserNotFoundError(
                "User not found."
            )

        return user

    def get_all(self) -> list[User]:

        return self._user_repository.get_all()

    # =========================================================
    # GET BY USERNAME
    # =========================================================

    def get_by_username(
        self,
        username: str,
    ) -> User:

        user = (
            self._user_repository.get_by_username(
                username.strip()
            )
        )

        if user is None:

            raise UserNotFoundError(
                "User not found."
            )

        return user

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        user_id: UUID,
        *,
        username: str,
        full_name: str,
        role_id: UUID,
        email: str | None = None,
        password: str | None = None,
    ) -> User:

        user = self.get_by_id(
            user_id
        )

        username = username.strip()
        full_name = full_name.strip()

        if not username:
            raise InvalidUsernameError(
                "Username cannot be empty."
            )

        if not full_name:
            raise InvalidFullNameError(
                "Full name cannot be empty."
            )

        email = self._validate_email(
            email
        )

        if password is not None and not password:
            raise InvalidPasswordError(
                "Password cannot be empty."
            )

        existing = (
            self._user_repository.get_by_username(
                username
            )
        )

        if (
            existing is not None
            and existing.id != user.id
        ):
            raise UserAlreadyExistsError(
                f'Username "{username}" already exists.'
            )

        if email is not None:

            existing = (
                self._user_repository.get_by_email(
                    email
                )
            )

            if (
                existing is not None
                and existing.id != user.id
            ):
                raise UserAlreadyExistsError(
                    f'Email "{email}" already exists.'
                )

        role = self._role_repository.get_by_id(
            role_id
        )

        if role is None:
            raise RoleNotFoundError(
                "Role not found."
            )

        user.sqlmodel_update(
            {
                "username": username,
                "full_name": full_name,
                "email": email,
                "role_id": role.id,
            }
        )

        if password is not None:

            user.password_hash = (
                self._password_hasher.hash_password(
                    password
                )
            )

        return self._user_repository.update(
            user
        )

    # =========================================================
    # CHANGE PASSWORD
    # =========================================================

    def change_password(
        self,
        user_id: UUID,
        password: str,
    ) -> User:

        user = self.get_by_id(
            user_id
        )

        if not password:
            raise InvalidPasswordError(
                "Password cannot be empty."
            )

        user.password_hash = (
            self._password_hasher.hash_password(
                password
            )
        )

        user.must_change_password = False

        return self._user_repository.update(
            user
        )

    # =========================================================
    # RESET PASSWORD
    # =========================================================

    def reset_password(
        self,
        user_id: UUID,
        password: str,
    ) -> User:
        """
        Reset a user's password after successful password
        recovery verification.

        Recovery-code validation and invalidation are handled
        by PasswordRecoveryService and SettingsService.
        """

        user = self.get_by_id(
            user_id
        )

        if not password:

            raise InvalidPasswordError(
                "Password cannot be empty."
            )

        user.password_hash = (
            self._password_hasher.hash_password(
                password
            )
        )

        user.must_change_password = False

        return self._user_repository.update(
            user
        )

    # =========================================================
    # GENERATE RECOVERY CODE
    # =========================================================

    def generate_recovery_code(
        self,
        user_id: UUID,
    ) -> str:
        """
        Generate a new recovery code for a user.

        This method is retained for compatibility with the
        existing user-service API.

        Application-wide password recovery is now handled by
        SettingsService.
        """

        raise NotImplementedError(
            "Recovery codes are application-wide and are "
            "managed by SettingsService."
        )

    # =========================================================
    # VERIFY RECOVERY CODE
    # =========================================================

    def verify_recovery_code(
        self,
        user_id: UUID,
        recovery_code: str,
    ) -> User:
        """
        User-specific recovery-code verification is no longer
        used.

        Application-wide recovery codes are verified by
        SettingsService.
        """

        raise NotImplementedError(
            "Recovery codes are application-wide and are "
            "verified by SettingsService."
        )

    # =========================================================
    # ACTIVATE / DEACTIVATE
    # =========================================================

    def set_active(
        self,
        user_id: UUID,
        is_active: bool,
    ) -> User:

        user = self.get_by_id(
            user_id
        )

        user.is_active = is_active

        return self._user_repository.update(
            user
        )

    def activate(
        self,
        user_id: UUID,
    ) -> User:

        return self.set_active(
            user_id,
            True,
        )

    def deactivate(
        self,
        user_id: UUID,
    ) -> User:

        return self.set_active(
            user_id,
            False,
        )
