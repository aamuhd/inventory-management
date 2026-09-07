import secrets
import string

from app.core.security.password_hasher import PasswordHasher

from app.modules.authentication.exceptions import (
    InvalidRecoveryCodeError,
)

from app.modules.settings.exceptions import (
    InvalidBusinessNameError,
    InvalidCurrencyError,
    InvalidInvoicePrefixError,
)

from app.modules.settings.models.settings import Settings

from app.modules.settings.repositories.settings_repository import (
    SettingsRepository,
)


class SettingsService:

    def __init__(
        self,
        repository: SettingsRepository,
        password_hasher: PasswordHasher,
    ) -> None:

        self._repository = repository
        self._password_hasher = password_hasher

    # =========================================================
    # GET
    # =========================================================

    def get(self) -> Settings:
        """
        Return application settings.

        If settings do not exist yet, create the default
        settings record.
        """

        settings = self._repository.get()

        if settings is None:

            settings = Settings(
                key=SettingsRepository.DEFAULT_KEY,
            )

            return self._repository.create(
                settings
            )

        return settings

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        *,
        business_name: str,
        business_address: str | None = None,
        business_phone: str | None = None,
        business_email: str | None = None,
        currency: str = "NGN",
        invoice_prefix: str = "INV",
        receipt_footer: str | None = None,
        low_stock_notifications: bool = True,
    ) -> Settings:

        # -----------------------------------------------------
        # NORMALIZE INPUT
        # -----------------------------------------------------

        business_name = business_name.strip()

        currency = currency.strip().upper()

        invoice_prefix = invoice_prefix.strip().upper()

        business_address = (
            business_address.strip()
            if business_address
            else None
        )

        business_phone = (
            business_phone.strip()
            if business_phone
            else None
        )

        business_email = (
            business_email.strip()
            if business_email
            else None
        )

        receipt_footer = (
            receipt_footer.strip()
            if receipt_footer
            else None
        )

        # -----------------------------------------------------
        # VALIDATE BUSINESS NAME
        # -----------------------------------------------------

        if not business_name:

            raise InvalidBusinessNameError(
                "Business name cannot be empty."
            )

        # -----------------------------------------------------
        # VALIDATE CURRENCY
        # -----------------------------------------------------

        if not currency:

            raise InvalidCurrencyError(
                "Currency cannot be empty."
            )

        # -----------------------------------------------------
        # VALIDATE INVOICE PREFIX
        # -----------------------------------------------------

        if not invoice_prefix:

            raise InvalidInvoicePrefixError(
                "Invoice prefix cannot be empty."
            )

        # -----------------------------------------------------
        # GET SETTINGS
        # -----------------------------------------------------

        settings = self.get()

        # -----------------------------------------------------
        # UPDATE
        # -----------------------------------------------------

        settings.sqlmodel_update(
            {
                "business_name": business_name,
                "business_address": business_address,
                "business_phone": business_phone,
                "business_email": business_email,
                "currency": currency,
                "invoice_prefix": invoice_prefix,
                "receipt_footer": receipt_footer,
                "low_stock_notifications": (
                    low_stock_notifications
                ),
            }
        )

        return self._repository.update(
            settings
        )

    # =========================================================
    # PASSWORD RECOVERY
    # =========================================================

    def generate_recovery_code(self) -> str:
        """
        Generate a new application-wide password recovery code.

        The plaintext recovery code is returned only once.

        Only the hashed version is stored in the database.

        Generating a new code invalidates the previous code.
        """

        alphabet = (
            string.ascii_uppercase
            + string.digits
        )

        parts = [
            "".join(
                secrets.choice(alphabet)
                for _ in range(4)
            )
            for _ in range(3)
        ]

        recovery_code = "-".join(
            parts
        )

        # -----------------------------------------------------
        # HASH RECOVERY CODE
        # -----------------------------------------------------

        recovery_code_hash = (
            self._password_hasher.hash_password(
                recovery_code
            )
        )

        # -----------------------------------------------------
        # STORE HASH
        # -----------------------------------------------------

        settings = self.get()

        settings.recovery_code_hash = (
            recovery_code_hash
        )

        settings.recovery_code_generated = True

        self._repository.update(
            settings
        )

        return recovery_code

    # =========================================================
    # VALIDATE RECOVERY CODE
    # =========================================================

    def validate_recovery_code(
        self,
        recovery_code: str,
    ) -> None:
        """
        Validate the application-wide password recovery code.

        The plaintext recovery code is never stored in the
        database.

        Raises InvalidRecoveryCodeError when the code is
        missing, unavailable, or incorrect.
        """

        recovery_code = (
            recovery_code.strip().upper()
        )

        if not recovery_code:

            raise InvalidRecoveryCodeError(
                "Please enter your recovery code."
            )

        settings = self.get()

        if not settings.recovery_code_generated:

            raise InvalidRecoveryCodeError(
                "Password recovery has not been configured."
            )

        if not settings.recovery_code_hash:

            raise InvalidRecoveryCodeError(
                "Password recovery has not been configured."
            )

        try:

            valid = (
                self._password_hasher.verify_password(
                    recovery_code,
                    settings.recovery_code_hash,
                )
            )

        except Exception as exc:

            raise InvalidRecoveryCodeError(
                "Invalid recovery code."
            ) from exc

        if not valid:

            raise InvalidRecoveryCodeError(
                "Invalid recovery code."
            )

    # =========================================================
    # INVALIDATE RECOVERY CODE
    # =========================================================

    def invalidate_recovery_code(self) -> Settings:
        """
        Invalidate the current application-wide recovery code.

        This is called after a successful password recovery so
        that the recovery code can only be used once.
        """

        settings = self.get()

        settings.recovery_code_hash = None

        settings.recovery_code_generated = False

        return self._repository.update(
            settings
        )
