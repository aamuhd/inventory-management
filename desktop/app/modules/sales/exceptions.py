class CustomerAlreadyExistsError(Exception):
    pass


class CustomerNotFoundError(Exception):
    pass


class InvalidCustomerNameError(Exception):
    pass



class SaleNotFoundError(Exception):
    pass


class SaleAlreadyExistsError(Exception):
    pass


class InvalidSaleStateError(Exception):
    pass


class EmptySaleError(Exception):
    pass


class DuplicateSaleItemError(Exception):
    pass


class SaleItemNotFoundError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


class InvalidInvoiceNumberError(Exception):
    pass

class SalesReturnError(Exception):
    """Base exception for sales return errors."""

class SalesReturnNotFoundError(SalesReturnError):
    """Raised when a sales return cannot be found."""

class SalesReturnItemNotFoundError(SalesReturnError):
    """Raised when a sales return item cannot be found."""

class SalesReturnAlreadyCompletedError(SalesReturnError):
    """Raised when attempting to modify a completed sales return."""

class EmptySalesReturnError(SalesReturnError):
    """Raised when trying to complete a sales return with no items."""


class OverReturnError(SalesReturnError):
    """Raised when the returned quantity exceeds the quantity sold."""

class InvalidSalesReturnError(SalesReturnError):
    """Raised when an invalid sales return operation is attempted."""



class InvalidSalesReturnStateError(SalesReturnError):
    pass


class InvalidReturnQuantityError(SalesReturnError):
    pass


class DuplicateSalesReturnItemError(SalesReturnError):
    pass


# Payment Exceptions

class PaymentError(Exception):
    """Base exception for payment-related errors."""


class PaymentNotFoundError(PaymentError):
    """Raised when a payment cannot be found."""


class InvalidPaymentAmountError(PaymentError):
    """Raised when a payment amount is invalid."""


class PaymentExceedsBalanceError(PaymentError):
    """Raised when a payment is greater than the outstanding balance."""


class PaymentSaleStateError(PaymentError):
    """Raised when payment is attempted for an invalid sale state."""

