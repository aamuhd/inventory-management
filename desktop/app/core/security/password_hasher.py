from argon2 import PasswordHasher as Argon2PasswordHasher
from argon2.exceptions import (
    HashingError,
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)

from .exceptions import (
    PasswordHashError,
    PasswordVerificationError,
)


class PasswordHasher:
    """
    Handles password hashing and verification.
    """

    def __init__(self) -> None:
        self._hasher = Argon2PasswordHasher()

    def hash_password(self, password: str) -> str:
        """
        Hash a plain text password.
        """
        try:
            return self._hasher.hash(password)
        except HashingError as exc:
            raise PasswordHashError(
                "Unable to hash password."
            ) from exc

    def verify_password(
        self,
        password: str,
        password_hash: str,
    ) -> bool:
        """
        Verify a password against its hash.
        """
        try:
            return self._hasher.verify(
                password_hash,
                password,
            )

        except VerifyMismatchError:
            return False

        except (
            InvalidHashError,
            VerificationError,
        ) as exc:
            raise PasswordVerificationError(
                "Password verification failed."
            ) from exc