from uuid import UUID

from sqlmodel import Session, select

from app.modules.inventory.models.purchase_order import (
    PurchaseOrder,
)
from app.modules.base_repo import BaseRepository


class PurchaseOrderRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def create(
        self,
        order: PurchaseOrder,
    ) -> PurchaseOrder:

        self._session.add(order)
        self._commit()
        self._session.refresh(order)

        return order

    def update(
        self,
        order: PurchaseOrder,
    ) -> PurchaseOrder:

        self._session.add(order)
        self._commit()
        self._session.refresh(order)

        return order

    def delete(
        self,
        order: PurchaseOrder,
    ) -> None:

        self._session.delete(order)
        self._commit()

    def get_by_id(
        self,
        order_id: UUID,
    ) -> PurchaseOrder | None:

        return self._session.get(
            PurchaseOrder,
            order_id,
        )

    def get_all(
        self,
    ) -> list[PurchaseOrder]:

        statement = select(
            PurchaseOrder,
        )

        return list(
            self._session.exec(statement),
        )

    def get_by_order_number(
        self,
        order_number: str,
    ) -> PurchaseOrder | None:

        statement = (
            select(PurchaseOrder)
            .where(
                PurchaseOrder.order_number == order_number,
            )
        )

        return self._session.exec(
            statement,
        ).first()

    def get_by_supplier(
        self,
        supplier_id: UUID,
    ) -> list[PurchaseOrder]:

        statement = (
            select(PurchaseOrder)
            .where(
                PurchaseOrder.supplier_id == supplier_id,
            )
        )

        return list(
            self._session.exec(statement),
        )
    
    