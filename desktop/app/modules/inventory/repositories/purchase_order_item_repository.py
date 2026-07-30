from uuid import UUID

from sqlmodel import Session, select

from app.modules.inventory.models.purchase_order_item import (
    PurchaseOrderItem,
)


class PurchaseOrderItemRepository:

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def create(
        self,
        item: PurchaseOrderItem,
    ) -> PurchaseOrderItem:

        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)

        return item

    def update(
        self,
        item: PurchaseOrderItem,
    ) -> PurchaseOrderItem:

        self._session.add(item)
        self._session.commit()
        self._session.refresh(item)

        return item

    def delete(
        self,
        item: PurchaseOrderItem,
    ) -> None:

        self._session.delete(item)
        self._session.commit()

    def get_by_id(
        self,
        item_id: UUID,
    ) -> PurchaseOrderItem | None:

        return self._session.get(
            PurchaseOrderItem,
            item_id,
        )

    def get_all(
        self,
    ) -> list[PurchaseOrderItem]:

        statement = select(
            PurchaseOrderItem,
        )

        return list(
            self._session.exec(statement),
        )

    def get_by_purchase_order(
        self,
        purchase_order_id: UUID,
    ) -> list[PurchaseOrderItem]:

        statement = (
            select(PurchaseOrderItem)
            .where(
                PurchaseOrderItem.purchase_order_id
                == purchase_order_id,
            )
        )

        return list(
            self._session.exec(statement),
        )

    def get_by_variant(
        self,
        variant_id: UUID,
    ) -> list[PurchaseOrderItem]:

        statement = (
            select(PurchaseOrderItem)
            .where(
                PurchaseOrderItem.product_variant_id
                == variant_id,
            )
        )

        return list(
            self._session.exec(statement),
        )
    
    
    def get_by_purchase_order_and_variant(
        self,
        purchase_order_id: UUID,
        variant_id: UUID,
    ) -> PurchaseOrderItem | None:

        statement = select(
            PurchaseOrderItem,
        ).where(
            PurchaseOrderItem.purchase_order_id == purchase_order_id,
            PurchaseOrderItem.product_variant_id == variant_id,
        )

        return self._session.exec(
            statement,
        ).first()