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