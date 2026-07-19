import sys

from PySide6.QtWidgets import QApplication

from app.modules.inventory.ui.category_window import CategoryWindow
from app.modules.inventory.services.category_service import CategoryService
from app.modules.inventory.repositories.category_repository import CategoryRepository

from sqlmodel import Session
from app.core.database.manager import DatabaseManager

db_manager = DatabaseManager()
engine = db_manager.engine

def main():
    with Session(engine) as session:
        repository = CategoryRepository(session)
        cat_service = CategoryService(repository)

        app = QApplication(sys.argv)

        window = CategoryWindow(cat_service)
        window.show()

        sys.exit(app.exec())

if __name__ == '__main__':
    main()