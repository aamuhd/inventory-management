from app.core.database.manager import DatabaseManager
from app.modules.inventory.models.category import Category
from app.modules.inventory.repositories.category_repository import CategoryRepository
from sqlmodel import Session


database_manager = DatabaseManager()
engine = database_manager.engine




def main():
    with Session(engine) as session:

        repository = CategoryRepository(session)
        category = Category(
            name="Electronics",
            description="Electronic products",
        )

        repository.add(category)

        print(repository.get_all())


if __name__ == '__main__':
    main()