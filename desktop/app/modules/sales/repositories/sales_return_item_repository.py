from uuid import UUID

from sqlmodel import Session, select

from app.modules.base_repo import BaseRepository
from app.modules.sales.models.sales_return_item import (
    SalesReturnItem,
)


class SalesReturnItemRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ):
        super().__init__(session)

    def create(
        self,
        item: SalesReturnItem,
    ) -> SalesReturnItem:

        self._session.add(item)
        self._commit()
        self._session.refresh(item)

        return item

    def get_by_id(
        self,
        item_id: UUID,
    ) -> SalesReturnItem | None:

        statement = (
            select(SalesReturnItem)
            .where(
                SalesReturnItem.id == item_id,
            )
        )

        return self._session.exec(statement).first()

    def update(
        self,
        item: SalesReturnItem,
    ) -> SalesReturnItem:

        self._session.add(item)
        self._commit()
        self._session.refresh(item)

        return item

    def delete(
        self,
        item: SalesReturnItem,
    ) -> None:

        self._session.delete(item)
        self._commit()

    def get_by_sales_return(
        self,
        sales_return_id: UUID,
    ) -> list[SalesReturnItem]:

        statement = (
            select(SalesReturnItem)
            .where(
                SalesReturnItem.sales_return_id == sales_return_id,
            )
        )

        return list(
            self._session.exec(statement),
        )

    def get_by_sale_item(
        self,
        sale_item_id: UUID,
    ) -> list[SalesReturnItem]:

        statement = (
            select(SalesReturnItem)
            .where(
                SalesReturnItem.sale_item_id == sale_item_id,
            )
        )

        return list(
            self._session.exec(statement),
        )