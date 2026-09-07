import secrets

from app.core.security.password_hasher import PasswordHasher


class RecoveryCodeManager:
    """
    Generates and verifies local password recovery codes.
    """

    def __init__(
        self,
        password_hasher: PasswordHasher,
    ) -> None:

        self._password_hasher = password_hasher

    # =========================================================
    # GENERATE
    # =========================================================

    @staticmethod
    def generate_code() -> str:
        """
        Generate a random recovery code.

        Example:
            7K4M-X9P2-Q8TW
        """

        raw_code = secrets.token_hex(6).upper()

        return (
            f"{raw_code[:4]}-"
            f"{raw_code[4:8]}-"
            f"{raw_code[8:12]}"
        )

    # =========================================================
    # HASH
    # =========================================================

    def hash_code(
        self,
        code: str,
    ) -> str:

        return self._password_hasher.hash_password(
            code
        )

    # =========================================================
    # VERIFY
    # =========================================================

    def verify_code(
        self,
        code: str,
        code_hash: str,
    ) -> bool:

        return self._password_hasher.verify_password(
            code,
            code_hash,
        )