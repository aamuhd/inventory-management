class CategoryError(Exception):
    """Base category exception."""


class CategoryAlreadyExistsError(CategoryError):
    """Raised when a category already exists."""


class CategoryNotFoundError(CategoryError):
    """Raised when a category cannot be found."""


class InvalidCategoryNameError(CategoryError):
    """Raised when the category name is invalid."""


# Product Exceptions

class ProductError(Exception):
    """Base category exception."""


class ProductAlreadyExistsError(ProductError):
    """Raised when a product already exists."""


class ProductNotFoundError(ProductError):
    """Raised when a product cannot be found."""


class InvalidProductNameError(ProductError):
    """Raised when the product name is invalid."""




# Product variant


class ProductVariantError(Exception):
    """Base category exception."""


class InvalidLengthError(ProductVariantError):
    """Raised when a length is not valid."""


class  InvalidPriceError(ProductVariantError):
    """Raised when a price is invalid."""


class InvalidStockQuantityError(ProductVariantError):
    """Raised when stock quantity is not valid."""


class  ProductVariantAlreadyExistsError(ProductVariantError):
    """Raised when a product variant already exists."""


class  ProductVariantNotFoundError(ProductVariantError):
    """Raised when a product variant cannot be found."""


# Stock Movement

class StockMovementNotFoundError(Exception):
    pass


class InvalidMovementQuantityError(Exception):
    pass


class InsufficientStockError(Exception):
    pass


# Supplier

class SupplierNotFoundError(Exception):
    pass


class SupplierAlreadyExistsError(Exception):
    pass


class InvalidSupplierNameError(Exception):
    pass



######

class InvalidPurchaseOrderStateError(Exception):
    pass


class PurchaseOrderNotFoundError(Exception):
    pass


######

class DuplicatePurchaseOrderItemError(Exception):
    pass

   
   


