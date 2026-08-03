from uuid import UUID

from sqlmodel import Session, select

from app.modules.sales.models.customer import Customer
from app.modules.base_repo import BaseRepository


class CustomerRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def create(
        self,
        customer: Customer,
    ) -> Customer:

        self._session.add(customer)
        self._commit()
        self._session.refresh(customer)

        return customer

    def update(
        self,
        customer: Customer,
    ) -> Customer:

        self._session.add(customer)
        self._commit()
        self._session.refresh(customer)

        return customer

    def delete(
        self,
        customer: Customer,
    ) -> None:

        self._session.delete(customer)
        self._commit()

    def get_by_id(
        self,
        customer_id: UUID,
    ) -> Customer | None:

        return self._session.get(
            Customer,
            customer_id,
        )

    def get_all(self) -> list[Customer]:

        statement = select(Customer)

        return list(
            self._session.exec(statement)
        )

    def get_by_name(
        self,
        name: str,
    ) -> Customer | None:

        statement = (
            select(Customer)
            .where(Customer.name == name)
        )

        return self._session.exec(statement).first()