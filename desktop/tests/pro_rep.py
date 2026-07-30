from app.core.database.manager import DatabaseManager
from app.modules.inventory.models.category import Category
from app.modules.inventory.repositories.product_repository import ProductRepository
from sqlmodel import Session
from app.modules.inventory.services.product_service import ProductService


database_manager = DatabaseManager()
engine = database_manager.engine





def main():
    with Session(engine) as session:

        repository = ProductRepository(session)
        pro_service = ProductService(product_repository=repository)
        #category_id = cat_service.get_by_id(1) 

        pro_service.create(name="Home of beauty", description="Abaya")
    

        print(pro_service.get_all())


if __name__ == '__main__':
    main()