from sqlmodel import Session, select

from app.modules.inventory.models.category import Category
from app.modules.base_repo import BaseRepository


class CategoryRepository(BaseRepository):

    def __init__(self, session: Session) -> None:
        self._session = session

    def add(self, category: Category) -> Category:
        self._session.add(category)
        self._commit()
        self._session.refresh(category)

        return category
    
    def update(self, category: Category) -> Category:
        self._session.add(category)
        self._commit()
        self._session.refresh(category)

        return category
    
    def delete(self, category: Category) -> None:
        self._session.delete(category)
        self._commit()

    def get_by_id(self, category_id: int) -> Category | None:
        return self._session.get(Category, category_id)
    
    def get_by_name(self, name: str) -> Category | None:
        statement = select(Category).where(Category.name == name)

        return self._session.exec(statement).first()
    
    def get_all(self) -> list[Category]:
        statement = select(Category).order_by(Category.name)

        return list(self._session.exec(statement))