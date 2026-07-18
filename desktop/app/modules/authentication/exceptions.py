class AuthenticationError(Exception):
    """Base authentication exception."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when the username or password is incorrect."""


class InactiveUserError(AuthenticationError):
    """Raised when a user account is inactive."""