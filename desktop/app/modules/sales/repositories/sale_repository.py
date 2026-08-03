from uuid import UUID

from sqlmodel import Session, select, desc
from sqlalchemy.exc import SQLAlchemyError

from app.modules.sales.models.sale import Sale
from app.modules.base_repo import BaseRepository



class SaleRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def create(
        self,
        sale: Sale,
    ) -> Sale:

        
        self._session.add(sale)
        self._commit()
        self._session.refresh(sale)

        return sale

       

    def update(
        self,
        sale: Sale,
    ) -> Sale:

        self._session.add(sale)
        self._commit()
        self._session.refresh(sale)

        return sale

    def delete(
        self,
        sale: Sale,
    ) -> None:

        self._session.delete(sale)
        self._commit()

    def get_by_id(
        self,
        sale_id: UUID,
    ) -> Sale | None:

        return self._session.get(
            Sale,
            sale_id,
        )

    def get_all(
        self,
    ) -> list[Sale]:

        

        statement = (
            select(Sale)
            .order_by(desc(Sale.sale_date))
        )

        return list(
            self._session.exec(statement)
        )

    def get_by_customer(
        self,
        customer_id: UUID,
    ) -> list[Sale]:

        statement = (
            select(Sale)
            .where(Sale.customer_id == customer_id)
        )

        return list(
            self._session.exec(statement)
        )

    def get_by_invoice_number(
        self,
        invoice_number: str,
    ) -> Sale | None:

        statement = (
            select(Sale)
            .where(Sale.invoice_number == invoice_number)
        )

        return self._session.exec(statement).first()