from uuid import UUID

from app.modules.inventory.exceptions import (
    InvalidSupplierNameError,
    SupplierAlreadyExistsError,
    SupplierHasDependenciesError,
    SupplierNotFoundError,
)
from app.modules.inventory.models.supplier import Supplier
from app.modules.inventory.repositories.supplier_repository import (
    SupplierRepository,
)


class SupplierService:

    def __init__(
        self,
        repository: SupplierRepository,
    ) -> None:
        self._repository = repository

    def create(
        self,
        *,
        name: str,
        contact_person: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
        notes: str | None = None,
    ) -> Supplier:

        name = name.strip()

        if not name:
            raise InvalidSupplierNameError(
                "Supplier name cannot be empty."
            )

        existing = self._repository.get_by_name(
            name,
        )

        if existing is not None:
            raise SupplierAlreadyExistsError(
                f'"{name}" already exists.'
            )

        supplier = Supplier(
            name=name,
            contact_person=contact_person,
            phone=phone,
            email=email,
            address=address,
            notes=notes,
        )

        return self._repository.create(
            supplier,
        )

    def get_by_id(
        self,
        supplier_id: UUID,
    ) -> Supplier:

        supplier = self._repository.get_by_id(
            supplier_id,
        )

        if supplier is None:
            raise SupplierNotFoundError(
                "Supplier not found."
            )

        return supplier

    def get_all(
        self,
    ) -> list[Supplier]:

        return self._repository.get_all()

    def update(
        self,
        supplier_id: UUID,
        *,
        name: str,
        contact_person: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
        notes: str | None = None,
    ) -> Supplier:

        supplier = self.get_by_id(
            supplier_id,
        )

        name = name.strip()

        if not name:
            raise InvalidSupplierNameError(
                "Supplier name cannot be empty."
            )

        existing = self._repository.get_by_name(
            name,
        )

        if (
            existing is not None
            and existing.id != supplier.id
        ):
            raise SupplierAlreadyExistsError(
                f'"{name}" already exists.'
            )

        supplier.name = name
        supplier.contact_person = contact_person
        supplier.phone = phone
        supplier.email = email
        supplier.address = address
        supplier.notes = notes

        return self._repository.update(
            supplier,
        )

    def delete(
        self,
        supplier_id: UUID,
    ) -> None:

        supplier = self.get_by_id(
            supplier_id,
        )

        if supplier.purchase_orders or supplier.returns:
            raise SupplierHasDependenciesError(
                "Cannot delete this supplier because it has "
                "purchase orders or supplier returns."
            )

        self._repository.delete(
            supplier,
        )