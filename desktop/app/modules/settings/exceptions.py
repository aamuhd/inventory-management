class SettingsError(Exception):
    """
    Base exception for the Settings module.
    """


class SettingsNotFoundError(SettingsError):
    """
    Raised when application settings cannot be found.
    """


class InvalidBusinessNameError(SettingsError):
    """
    Raised when the business name is invalid.
    """


class InvalidCurrencyError(SettingsError):
    """
    Raised when the currency is invalid.
    """


class InvalidInvoicePrefixError(SettingsError):
    """
    Raised when the invoice prefix is invalid.
    """
