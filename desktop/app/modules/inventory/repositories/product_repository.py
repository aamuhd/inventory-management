from uuid import UUID

from sqlmodel import Session, select

from app.modules.inventory.models.product import Product
from app.modules.base_repo import BaseRepository



class ProductRepository(BaseRepository):
    """
    Handles database operations for Product.
    """

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, product: Product) -> Product:
        self._session.add(product)
        self._commit()
        self._session.refresh(product)
        return product

    def get_by_id(self, product_id: UUID) -> Product | None:
        return self._session.get(Product, product_id)

    
    def get_by_name_and_brand(
        self,
        name: str,
        brand: str | None,
    ) -> Product | None:

        statement = select(Product).where(
            Product.name == name,
            Product.brand == brand,
        )

        return self._session.exec(statement).first()

    def get_all(self) -> list[Product]:
        statement = select(Product).order_by(Product.name)
        return list(self._session.exec(statement))

    def update(self, product: Product) -> Product:
        self._session.add(product)
        self._commit()
        self._session.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self._session.delete(product)
        self._commit()