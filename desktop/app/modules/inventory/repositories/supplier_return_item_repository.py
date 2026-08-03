from uuid import UUID

from sqlmodel import Session, select

from app.modules.inventory.models.supplier_return_item import (
    SupplierReturnItem,
)
from app.modules.base_repo import BaseRepository


class SupplierReturnItemRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ) -> None:

        self._session = session

    def create(
        self,
        item: SupplierReturnItem,
    ) -> SupplierReturnItem:

        self._session.add(
            item,
        )

        self._commit()

        self._session.refresh(
            item,
        )

        return item

    def update(
        self,
        item: SupplierReturnItem,
    ) -> SupplierReturnItem:

        self._session.add(
            item,
        )

        self._commit()

        self._session.refresh(
            item,
        )

        return item

    def get_by_id(
        self,
        item_id: UUID,
    ) -> SupplierReturnItem | None:

        return self._session.get(
            SupplierReturnItem,
            item_id,
        )

    def get_by_supplier_return(
        self,
        supplier_return_id: UUID,
    ) -> list[SupplierReturnItem]:

        statement = (
            select(
                SupplierReturnItem,
            )
            .where(
                SupplierReturnItem.supplier_return_id
                == supplier_return_id,
            )
        )

        return list(
            self._session.exec(
                statement,
            )
        )

    def get_by_supplier_return_and_variant(
        self,
        supplier_return_id: UUID,
        variant_id: UUID,
    ) -> SupplierReturnItem | None:

        statement = (
            select(
                SupplierReturnItem,
            )
            .where(
                SupplierReturnItem.supplier_return_id
                == supplier_return_id,
                SupplierReturnItem.variant_id
                == variant_id,
            )
        )

        return self._session.exec(
            statement,
        ).first()

    def delete(
        self,
        item: SupplierReturnItem,
    ) -> None:

        self._session.delete(
            item,
        )

        self._commit()