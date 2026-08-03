from uuid import UUID

from sqlmodel import Session, select

from app.modules.sales.models.sale_item import SaleItem
from app.modules.base_repo import BaseRepository


class SaleItemRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def create(
        self,
        item: SaleItem,
    ) -> SaleItem:

        self._session.add(item)
        self._commit()
        self._session.refresh(item)

        return item

    def update(
        self,
        item: SaleItem,
    ) -> SaleItem:

        self._session.add(item)
        self._commit()
        self._session.refresh(item)

        return item

    def delete(
        self,
        item: SaleItem,
    ) -> None:

        self._session.delete(item)
        self._commit()

    def get_by_id(
        self,
        item_id: UUID,
    ) -> SaleItem | None:

        return self._session.get(
            SaleItem,
            item_id,
        )

    def get_by_sale(
        self,
        sale_id: UUID,
    ) -> list[SaleItem]:

        statement = (
            select(SaleItem)
            .where(SaleItem.sale_id == sale_id)
        )

        return list(
            self._session.exec(statement)
        )

    def get_by_sale_and_variant(
        self,
        sale_id: UUID,
        variant_id: UUID,
    ) -> SaleItem | None:

        statement = (
            select(SaleItem)
            .where(
                SaleItem.sale_id == sale_id,
                SaleItem.product_variant_id == variant_id,
            )
        )

        return self._session.exec(statement).first()