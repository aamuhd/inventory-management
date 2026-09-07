from uuid import UUID

from sqlmodel import Session, select

from app.modules.inventory.models.product_variant import ProductVariant
from app.modules.base_repo import BaseRepository


class ProductVariantRepository(BaseRepository):

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        variant: ProductVariant,
    ) -> ProductVariant:

        self._session.add(variant)
        self._commit()
        self._session.refresh(variant)

        return variant
    
    def update(
        self,
        variant: ProductVariant,
    ) -> ProductVariant:

        self._session.add(variant)
        self._commit()
        self._session.refresh(variant)

        return variant

    def update_stock(
        self,
        variant: ProductVariant,
    ) -> ProductVariant:

        self._session.add(variant)
        self._session.flush()

        return variant

    def delete(
        self,
        variant: ProductVariant,
    ) -> None:

        self._session.delete(variant)
        self._commit()

    def get_by_id(
        self,
        variant_id: UUID,
    ) -> ProductVariant | None:

        return self._session.get(
            ProductVariant,
            variant_id,
        )

    def get_all(self) -> list[ProductVariant]:

        self._session.expire_all()

        statement = select(ProductVariant)

        return list(
            self._session.exec(statement)
        )

    def get_by_product(
        self,
        product_id: UUID,
    ) -> list[ProductVariant]:

        self._session.expire_all()

        statement = (
            select(ProductVariant)
            .where(
                ProductVariant.product_id == product_id
            )
        )

        return list(
            self._session.exec(statement)
        )

    def get_by_product_and_length(
        self,
        product_id: UUID,
        length: int,
    ) -> ProductVariant | None:

        statement = (
            select(ProductVariant)
            .where(
                ProductVariant.product_id == product_id,
                ProductVariant.length == length,
            )
        )

        return self._session.exec(statement).first()
    
    
    def commit(self) -> None:
        self._commit()

    def rollback(self) -> None:
        self._session.rollback()