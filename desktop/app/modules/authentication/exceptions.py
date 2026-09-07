class AuthenticationError(Exception):
    """Base authentication exception."""


class InvalidCredentialsError(AuthenticationError):
    """Raised when the username or password is incorrect."""


class InactiveUserError(AuthenticationError):
    """Raised when a user account is inactive."""


class PasswordRecoveryError(AuthenticationError):
    """Base exception for password recovery."""


# =========================================================
# USER EXCEPTIONS
# =========================================================


class InvalidUsernameError(Exception):
    """Raised when a username is invalid."""


class InvalidFullNameError(Exception):
    """Raised when a full name is invalid."""


class UserAlreadyExistsError(Exception):
    """Raised when a user already exists."""


class UserNotFoundError(Exception):
    """Raised when a user cannot be found."""


class InvalidEmailError(Exception):
    """Raised when an email address is invalid."""


class InvalidPasswordError(Exception):
    """Raised when a password is invalid."""


# =========================================================
# ROLE EXCEPTIONS
# =========================================================


class InvalidRoleNameError(Exception):
    """Raised when a role name is invalid."""


class RoleAlreadyExistsError(Exception):
    """Raised when a role already exists."""


class RoleNotFoundError(Exception):
    """Raised when a role cannot be found."""


class InvalidRecoveryCodeError(AuthenticationError):
    """Raised when a recovery code is invalid."""


class RecoveryCodeNotConfiguredError(AuthenticationError):
    """Raised when password recovery has not been configured."""