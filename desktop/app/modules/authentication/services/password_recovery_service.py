from app.modules.authentication.exceptions import (
    InvalidRecoveryCodeError,
    UserNotFoundError,
)

from app.modules.authentication.models.user import User

from app.modules.authentication.services.user_service import (
    UserService,
)

from app.modules.settings.services.settings_service import (
    SettingsService,
)


class PasswordRecoveryService:
    """
    Handles local password recovery using the
    application-wide recovery code.
    """

    def __init__(
        self,
        user_service: UserService,
        settings_service: SettingsService,
    ) -> None:

        self._user_service = user_service
        self._settings_service = settings_service

    # =========================================================
    # RESET PASSWORD
    # =========================================================

    def reset_password(
        self,
        *,
        username: str,
        recovery_code: str,
        new_password: str,
    ) -> User:

        username = username.strip()

        recovery_code = (
            recovery_code.strip().upper()
        )

        # -----------------------------------------------------
        # USERNAME
        # -----------------------------------------------------

        if not username:

            raise InvalidRecoveryCodeError(
                "Please enter your username."
            )

        # -----------------------------------------------------
        # RECOVERY CODE
        # -----------------------------------------------------

        if not recovery_code:

            raise InvalidRecoveryCodeError(
                "Please enter your recovery code."
            )

        # -----------------------------------------------------
        # FIND USER
        # -----------------------------------------------------

        try:

            user = (
                self._user_service.get_by_username(
                    username
                )
            )

        except UserNotFoundError as exc:

            raise InvalidRecoveryCodeError(
                "Unable to recover this account."
            ) from exc

        # -----------------------------------------------------
        # VERIFY MASTER RECOVERY CODE
        # -----------------------------------------------------

        self._settings_service.validate_recovery_code(
            recovery_code
        )

        # -----------------------------------------------------
        # RESET PASSWORD
        # -----------------------------------------------------

        return self._user_service.reset_password(
            user.id,
            new_password,
        )
