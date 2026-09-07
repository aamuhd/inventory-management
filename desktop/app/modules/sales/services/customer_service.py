from uuid import UUID

from app.modules.sales.exceptions import (
    CustomerAlreadyExistsError,
    CustomerNotFoundError,
    InvalidCustomerNameError,
    
)

from app.modules.sales.models.customer import Customer
from app.modules.sales.repositories.customer_repository import CustomerRepository



class CustomerService:

    def __init__(
        self,
        repository: CustomerRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        *,
        name: str,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
    ) -> Customer:

        name = name.strip()

        if not name:
            raise InvalidCustomerNameError(
                "Customer name cannot be empty."
            )

        existing = self._repository.get_by_name(
            name,
        )

        if existing is not None:
            raise CustomerAlreadyExistsError(
                f'"{name}" already exists.'
            )

        customer = Customer(
            name=name,
            phone=phone,
            email=email,
            address=address,
        )

        return self._repository.create(
            customer,
        )

    def get_by_id(
        self,
        customer_id: UUID,
    ) -> Customer:

        customer = self._repository.get_by_id(
            customer_id,
        )

        if customer is None:
            raise CustomerNotFoundError(
                "Customer not found."
            )

        return customer

    def get_all(
        self,
    ) -> list[Customer]:

        return self._repository.get_all()

    def update(
        self,
        customer_id: UUID,
        *,
        name: str,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
    ) -> Customer:

        customer = self.get_by_id(
            customer_id,
        )

        name = name.strip()

        if not name:
            raise InvalidCustomerNameError(
                "Customer name cannot be empty."
            )

        existing = self._repository.get_by_name(
            name,
        )

        if (
            existing is not None
            and existing.id != customer.id
        ):
            raise CustomerAlreadyExistsError(
                f'"{name}" already exists.'
            )

        customer.name = name
        customer.phone = phone
        customer.email = email
        customer.address = address

        return self._repository.update(
            customer,
        )

    def delete(
        self,
        customer_id: UUID,
    ) -> None:

        customer = self.get_by_id(
            customer_id,
        )

        self._repository.delete(
            customer,
        )