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






