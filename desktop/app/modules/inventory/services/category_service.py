from app.modules.inventory.models.category import Category
from app.modules.inventory.repositories.category_repository import (
    CategoryRepository,
)
from app.modules.inventory.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    InvalidCategoryNameError,
)


class CategoryService:
    def __init__(
        self,
        repository: CategoryRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        name: str,
        description: str,
    ) -> Category:

        name = name.strip()

        if not name:
            raise InvalidCategoryNameError(
                "Category name cannot be empty."
            )

        if self._repository.get_by_name(name):
            raise CategoryAlreadyExistsError(
                f'"{name}" already exists.'
            )

        category = Category(
            name=name,
            description=description.strip(),
        )

        return self._repository.add(category)
    
    def get_all(self) -> list[Category]:
        return self._repository.get_all()
    
    def get_by_id(
        self,
        category_id: int,
    ) -> Category | None:
        return self._repository.get_by_id(category_id)
    
    def update(
        self,
        category_id: int,
        name: str,
        description: str,
    ) -> Category:

        category = self._repository.get_by_id(category_id)

        if category is None:
            raise CategoryNotFoundError(
                "Category not found."
            )

        category.name = name.strip()
        category.description = description.strip()

        return self._repository.update(category)
        
    def delete(
        self,
        category_id: int,
    ) -> None:
        category = self._repository.get_by_id(category_id)
        if category is None:
            raise CategoryNotFoundError("Category not found.")
        
        self._repository.delete(category)