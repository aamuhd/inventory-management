from uuid import UUID

from sqlmodel import Session, select

from app.modules.inventory.models.supplier_return import SupplierReturn


class SupplierReturnRepository:

    def __init__(
        self,
        session: Session,
    ) -> None:

        self._session = session

    def create(
        self,
        supplier_return: SupplierReturn,
    ) -> SupplierReturn:

        self._session.add(
            supplier_return,
        )

        self._session.commit()

        self._session.refresh(
            supplier_return,
        )

        return supplier_return

    def update(
        self,
        supplier_return: SupplierReturn,
    ) -> SupplierReturn:

        self._session.add(
            supplier_return,
        )

        self._session.commit()

        self._session.refresh(
            supplier_return,
        )

        return supplier_return

    def get_by_id(
        self,
        supplier_return_id: UUID,
    ) -> SupplierReturn | None:

        return self._session.get(
            SupplierReturn,
            supplier_return_id,
        )

    def get_by_return_number(
        self,
        return_number: str,
    ) -> SupplierReturn | None:

        statement = (
            select(SupplierReturn)
            .where(
                SupplierReturn.return_number == return_number,
            )
        )

        return self._session.exec(
            statement,
        ).first()

    def get_all(
        self,
    ) -> list[SupplierReturn]:

        statement = select(
            SupplierReturn,
        )

        return list(
            self._session.exec(
                statement,
            )
        )

    def delete(
        self,
        supplier_return: SupplierReturn,
    ) -> None:

        self._session.delete(
            supplier_return,
        )

        self._session.commit()