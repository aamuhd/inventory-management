from datetime import date
from uuid import UUID

from app.modules.inventory.enums.supplier_return_status import SupplierReturnStatus
from app.modules.inventory.models.supplier_return import SupplierReturn
from app.modules.inventory.models.supplier_return_item import SupplierReturnItem
from app.modules.inventory.repositories.supplier_return_item_repository import (
    SupplierReturnItemRepository,
)
from app.modules.inventory.repositories.supplier_return_repository import (
    SupplierReturnRepository,
)
from app.modules.inventory.services.stock_movement_service import StockMovementService
from app.modules.inventory.exceptions import (
    DuplicateSupplierReturnError,
    DuplicateSupplierReturnItemError,
    EmptySupplierReturnError,
    InvalidSupplierReturnStateError, 
    SupplierReturnItemNotFoundError, 
    SupplierReturnNotFoundError
) 


class SupplierReturnService:

    def __init__(
        self,
        return_repository: SupplierReturnRepository,
        item_repository: SupplierReturnItemRepository,
        stock_movement_service: StockMovementService,
    ) -> None:

        self._return_repository = return_repository
        self._item_repository = item_repository
        self._stock_movement_service = stock_movement_service

    def create(
        self,
        supplier_id: UUID,
        purchase_order_id: UUID | None,
        return_number: str,
        return_date: date,
        notes: str | None = None,
    ) -> SupplierReturn:

        self._validate_duplicate_return_number(
            return_number,
        )

        supplier_return = SupplierReturn(
            supplier_id=supplier_id,
            purchase_order_id=purchase_order_id,
            return_number=return_number,
            return_date=return_date,
            notes=notes,
        )

        return self._return_repository.create(
            supplier_return,
        )
    
    def get_by_id(
        self,
        supplier_return_id: UUID,
    ) -> SupplierReturn:

        supplier_return = self._return_repository.get_by_id(
            supplier_return_id,
        )

        if supplier_return is None:
            raise SupplierReturnNotFoundError(
                "Supplier return not found."
            )

        return supplier_return
    
    def get_all(self) -> list[SupplierReturn]:
        return self._return_repository.get_all()
    
    def delete(
        self,
        supplier_return_id: UUID,
    ) -> None:

        supplier_return = self.get_by_id(
            supplier_return_id,
        )

        if supplier_return.status != SupplierReturnStatus.DRAFT:
            raise InvalidSupplierReturnStateError(
                "Only draft supplier returns can be deleted."
            )

        self._return_repository.delete(
            supplier_return,
        )

    def update(
        self,
        supplier_return_id: UUID,
        supplier_id: UUID,
        purchase_order_id: UUID | None,
        return_number: str,
        return_date: date,
        notes: str | None = None,
    ) -> SupplierReturn:

        supplier_return = self.get_by_id(
            supplier_return_id,
        )

        self._validate_draft(
            supplier_return,
        )

        existing = self._return_repository.get_by_return_number(
            return_number,
        )

        if (
            existing is not None
            and existing.id != supplier_return.id
        ):
            raise DuplicateSupplierReturnError(
                "Return number already exists."
            )

        supplier_return.supplier_id = supplier_id
        supplier_return.purchase_order_id = purchase_order_id
        supplier_return.return_number = return_number
        supplier_return.return_date = return_date
        supplier_return.notes = notes

        return self._return_repository.update(
            supplier_return,
        )
    
    def get_item(
        self,
        item_id: UUID,
    ) -> SupplierReturnItem:

        item = self._item_repository.get_by_id(
            item_id,
        )

        if item is None:
            raise SupplierReturnItemNotFoundError(
                "Supplier return item not found."
            )

        return item
    
    def _validate_duplicate_return_number(
        self,
        return_number: str,
    ) -> None:

        if (
            self._return_repository.get_by_return_number(
                return_number,
            )
            is not None
        ):
            raise DuplicateSupplierReturnError(
                "Return number already exists."
            )
        
    def _validate_draft(
        self,
        supplier_return: SupplierReturn,
    ) -> None:

        if (
            supplier_return.status
            != SupplierReturnStatus.DRAFT
        ):
            raise InvalidSupplierReturnStateError(
                "Only draft supplier returns can be modified."
            )
        
    def add_item(
        self,
        supplier_return_id: UUID,
        variant_id: UUID,
        quantity: int,
        reason: str,
    ) -> SupplierReturnItem:

        supplier_return = self.get_by_id(
            supplier_return_id,
        )

        self._validate_draft(
            supplier_return,
        )

        self._validate_duplicate_item(
            supplier_return_id,
            variant_id,
        )

        item = SupplierReturnItem(
            supplier_return_id=supplier_return_id,
            variant_id=variant_id,
            quantity=quantity,
            reason=reason,
        )

        return self._item_repository.create(
            item,
        )
    
    def update_item(
        self,
        item_id: UUID,
        quantity: int,
        reason: str,
    ) -> SupplierReturnItem:

        item = self.get_item(
            item_id,
        )

        supplier_return = self.get_by_id(
            item.supplier_return_id,
        )

        self._validate_draft(
            supplier_return,
        )

        item.quantity = quantity
        item.reason = reason

        return self._item_repository.update(
            item,
        )
    
    def delete_item(
        self,
        item_id: UUID,
    ) -> None:

        item = self.get_item(
            item_id,
        )

        supplier_return = self.get_by_id(
            item.supplier_return_id,
        )

        self._validate_draft(
            supplier_return,
        )

        self._item_repository.delete(
            item,
        )

    def _validate_duplicate_item(
        self,
        supplier_return_id: UUID,
        variant_id: UUID,
    ) -> None:

        item = (
            self._item_repository.get_by_supplier_return_and_variant(
                supplier_return_id,
                variant_id,
            )
        )

        if item is not None:
            raise DuplicateSupplierReturnItemError(
                "Variant already exists in supplier return."
            )
        
    def _validate_not_empty(
        self,
        supplier_return_id: UUID,
    ) -> None:

        items = (
            self._item_repository.get_by_supplier_return(
                supplier_return_id,
            )
        )

        if not items:
            raise EmptySupplierReturnError(
                "Supplier return contains no items."
            )
        
    def submit(
        self,
        supplier_return_id: UUID,
    ) -> SupplierReturn:

        supplier_return = self.get_by_id(
            supplier_return_id,
        )

        self._validate_draft(
            supplier_return,
        )

        self._validate_not_empty(
            supplier_return.id,
        )

        items = (
            self._item_repository.get_by_supplier_return(
                supplier_return.id,
            )
        )

        try:

            for item in items:

                self._stock_movement_service.damage_stock(
                    variant_id=item.variant_id,
                    quantity=item.quantity,
                    reference=supplier_return.return_number,
                    notes=item.reason,
                )

            supplier_return.status = (
                SupplierReturnStatus.SUBMITTED
            )

            supplier_return = (
                self._return_repository.update(
                    supplier_return,
                )
            )

        except Exception:
            raise

        return supplier_return