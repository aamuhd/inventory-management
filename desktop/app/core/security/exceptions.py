class PasswordHashError(Exception):
    """
    Raised when password hashing fails.
    """


class PasswordVerificationError(Exception):
    """
    Raised when password verification fails unexpectedly.
    """