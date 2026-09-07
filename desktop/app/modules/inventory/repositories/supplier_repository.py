from uuid import UUID

from sqlmodel import Session, select

from app.modules.inventory.models.supplier import Supplier
from app.modules.base_repo import BaseRepository


class SupplierRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def create(
        self,
        supplier: Supplier,
    ) -> Supplier:

        self._session.add(supplier)
        self._commit()
        self._session.refresh(supplier)

        return supplier

    def update(
        self,
        supplier: Supplier,
    ) -> Supplier:

        self._session.add(supplier)
        self._commit()
        self._session.refresh(supplier)

        return supplier

    def delete(
        self,
        supplier: Supplier,
    ) -> None:

        self._session.delete(supplier)
        self._commit()

    def get_by_id(
        self,
        supplier_id: UUID,
    ) -> Supplier | None:

        return self._session.get(
            Supplier,
            supplier_id,
        )

    def get_all(
        self,
    ) -> list[Supplier]:

        statement = select(Supplier)

        return list(
            self._session.exec(statement)
        )

    def get_by_name(
        self,
        name: str,
    ) -> Supplier | None:

        statement = (
            select(Supplier)
            .where(Supplier.name == name)
        )

        return self._session.exec(
            statement
        ).first()

    def has_related_records(
        self,
        supplier: Supplier,
    ) -> bool:

        return bool(
            supplier.purchase_orders
            or supplier.returns
        )