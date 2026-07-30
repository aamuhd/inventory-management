import sys

from PySide6.QtWidgets import QApplication

from app.modules.inventory.ui.category_window import CategoryWindow
from app.modules.inventory.services.category_service import CategoryService
from app.modules.inventory.repositories.category_repository import CategoryRepository

from sqlmodel import Session
from app.core.database.manager import DatabaseManager
from app.modules.inventory.repositories.product_repository import ProductRepository
from app.modules.inventory.services.product_service import ProductService
from app.modules.inventory.ui.product_window import ProductWindow

db_manager = DatabaseManager()
engine = db_manager.engine

def main():
    with Session(engine) as session:
        repository = ProductRepository(session)
        pro_service = ProductService(repository)

        cat_repository = CategoryRepository(session)
        cat_service = CategoryService(cat_repository)

        app = QApplication(sys.argv)

        window = ProductWindow(pro_service, cat_service)
        window.show()

        sys.exit(app.exec())

if __name__ == '__main__':
    main()