from app.core.database.manager import DatabaseManager
from app.modules.inventory.models.category import Category
from app.modules.inventory.repositories.category_repository import CategoryRepository
from sqlmodel import Session
from app.modules.inventory.services.category_service import CategoryService


database_manager = DatabaseManager()
engine = database_manager.engine





def main():
    with Session(engine) as session:

        repository = CategoryRepository(session)
        cat_service = CategoryService(repository=repository)
        #category_id = cat_service.get_by_id(1) 

        cat_service.create(name="Home of beauty", description="Abaya")
    

        print(cat_service.get_all())


if __name__ == '__main__':
    main()