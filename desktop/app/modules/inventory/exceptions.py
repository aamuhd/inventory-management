class CategoryError(Exception):
    """Base category exception."""


class CategoryAlreadyExistsError(CategoryError):
    """Raised when a category already exists."""


class CategoryNotFoundError(CategoryError):
    """Raised when a category cannot be found."""


class InvalidCategoryNameError(CategoryError):
    """Raised when the category name is invalid."""