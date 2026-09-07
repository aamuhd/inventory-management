from datetime import date
from decimal import Decimal
from uuid import UUID

from app.modules.inventory.services.product_variant_service import ProductVariantService
from app.modules.inventory.services.stock_movement_service import StockMovementService
from app.modules.sales.services.sale_service import SaleService

from app.modules.sales.enums.sale_status import SaleStatus
from app.modules.sales.enums.sales_return_status import SalesReturnStatus

from app.modules.sales.exceptions import (
    EmptySalesReturnError,
    InvalidReturnQuantityError, 
    InvalidSaleStateError, 
    InvalidSalesReturnStateError, 
    OverReturnError, 
    SaleItemNotFoundError, 
    SalesReturnAlreadyCompletedError, 
    SalesReturnItemNotFoundError, 
    SalesReturnNotFoundError
)

from app.modules.sales.models.sales_return import SalesReturn
from app.modules.sales.models.sales_return_item import SalesReturnItem

from app.modules.sales.repositories.sale_item_repository import SaleItemRepository
from app.modules.sales.repositories.sales_return_item_repository import SalesReturnItemRepository
from app.modules.sales.repositories.sales_return_repository import SalesReturnRepository
from app.modules.inventory.enums.movement_type import MovementType



class SalesReturnService:

    def __init__(
        self,
        sales_return_repository: SalesReturnRepository,
        sales_return_item_repository: SalesReturnItemRepository,
        sale_service: SaleService,
        sale_item_repository: SaleItemRepository,
        stock_movement_service: StockMovementService,
        product_variant_service: ProductVariantService,
    ):

        self._repository = sales_return_repository
        self._item_repository = sales_return_item_repository
        self._sale_service = sale_service
        self._sale_item_repository = sale_item_repository
        self._product_variant_service = product_variant_service
        self._stock_movement_service = stock_movement_service
      
    def create(
        self,
        sale_id: UUID,
        #return_number: str,
        return_date: date,
        reason: str | None = None,
    ) -> SalesReturn:

        sale = self._sale_service.get_by_id(
            sale_id,
        )

        if sale.status != SaleStatus.COMPLETED:
            raise InvalidSaleStateError(
                "Only completed sales can be returned."
            )

        sales_return = SalesReturn(
            sale_id=sale_id,
            return_number=self.generate_return_number(),
            return_date=return_date,
            reason=reason,
            status=SalesReturnStatus.DRAFT,
            total_amount=Decimal("0.00"),
        )

        return self._repository.create(
            sales_return,
        )

    def get_by_id(
        self,
        sales_return_id: UUID,
    ) -> SalesReturn:

        sales_return = self._repository.get_by_id(
            sales_return_id,
        )

        if sales_return is None:
            raise SalesReturnNotFoundError(
                "Sales return not found."
            )

        return sales_return

    def get_all(
        self,
    ) -> list[SalesReturn]:

        return self._repository.get_all()

    def delete(
        self,
        sales_return_id: UUID,
    ) -> None:

        sales_return = self.get_by_id(
            sales_return_id,
        )

        if sales_return.status != SalesReturnStatus.DRAFT:
            raise SalesReturnAlreadyCompletedError(
                "Completed returns cannot be deleted."
            )

        self._repository.delete(
            sales_return,
        )

    def update(
        self,
        sales_return_id: UUID,
        return_date: date,
        reason: str | None,
    ) -> SalesReturn:

        sales_return = self.get_by_id(
            sales_return_id,
        )

        if sales_return.status != SalesReturnStatus.DRAFT:
            raise SalesReturnAlreadyCompletedError(
                "Completed returns cannot be edited."
            )

        sales_return.return_date = return_date
        sales_return.reason = reason

        return self._repository.update(
            sales_return,
        )

    def add_item(
        self,
        sales_return_id: UUID,
        sale_item_id: UUID,
        quantity: int,
    ) -> SalesReturnItem:

        sales_return = self.get_by_id(
            sales_return_id,
        )

        if sales_return.status != SalesReturnStatus.DRAFT:
            raise InvalidSalesReturnStateError(
                "Sales return has already been completed."
            )

        sale_item = self._sale_item_repository.get_by_id(
            sale_item_id,
        )

        if sale_item is None:
            raise SaleItemNotFoundError(
                "Sale item not found."
            )

        previous_returns = (
            self._item_repository.get_by_sale_item(
                sale_item_id,
            )
        )

        returned_quantity = sum(
            item.quantity
            for item in previous_returns
        )

        available_quantity = (
            sale_item.quantity - returned_quantity
        )

        if quantity > available_quantity:
            raise InvalidReturnQuantityError(
                "Return quantity exceeds available quantity."
            )

        return_item = SalesReturnItem(
            sales_return_id=sales_return_id,
            sale_item_id=sale_item_id,
            quantity=quantity,
            unit_price=sale_item.unit_price,
        )

        self._item_repository.create(
            return_item,
        )

        self._recalculate_total(
            sales_return_id,
        )

        return return_item

    def _recalculate_total(
        self,
        sales_return_id: UUID,
    ):

        sales_return = self.get_by_id(
            sales_return_id,
        )

        total = Decimal("0.00")

        for item in sales_return.items:

            total += (
                item.quantity
                * item.unit_price
            )

        sales_return.total_amount = total

        self._repository.update(
            sales_return,
        )

    def update_item(
        self,
        return_item_id: UUID,
        quantity: int,
    ) -> SalesReturnItem:

        return_item = self._item_repository.get_by_id(
            return_item_id,
        )

        if return_item is None:
            raise SalesReturnItemNotFoundError(
                "Sales return item not found."
            )

        sales_return = self.get_by_id(
            return_item.sales_return_id,
        )

        if sales_return.status != SalesReturnStatus.DRAFT:
            raise SalesReturnAlreadyCompletedError(
                "Completed returns cannot be modified."
            )

        sale_item = self._sale_item_repository.get_by_id(
            return_item.sale_item_id,
        )

        if sale_item is None:
            raise SaleItemNotFoundError(
                "Sale item not found."
            )
                
        previous_returns = (
            self._item_repository.get_by_sale_item(
                sale_item.id,
            )
        )

        returned_quantity = sum(
            item.quantity
            for item in previous_returns
            if item.id != return_item.id
        )

        outstanding = (
            sale_item.quantity - returned_quantity
        )

        if quantity > outstanding:
            raise OverReturnError(
                f"Only {outstanding} item(s) can still be returned."
            )

        return_item.quantity = quantity

        return_item = self._item_repository.update(
            return_item,
        )

        self._recalculate_total(
            sales_return.id,
        )

        return return_item

    def delete_item(
        self,
        return_item_id: UUID,
    ) -> None:

        return_item = self._item_repository.get_by_id(
            return_item_id,
        )

        if return_item is None:
            raise SalesReturnItemNotFoundError(
                "Sales return item not found."
            )

        sales_return = self.get_by_id(
            return_item.sales_return_id,
        )

        if sales_return.status != SalesReturnStatus.DRAFT:
            raise SalesReturnAlreadyCompletedError(
                "Completed returns cannot be modified."
            )

        self._item_repository.delete(
            return_item,
        )

        self._recalculate_total(
            sales_return.id,
        )

    def complete(
        self,
        sales_return_id: UUID,
    ) -> None:

        sales_return = self.get_by_id(
            sales_return_id,
        )

        if sales_return.status != SalesReturnStatus.DRAFT:
            raise SalesReturnAlreadyCompletedError(
                "Sales return has already been completed."
            )

        items = self._item_repository.get_by_sales_return(
            sales_return_id,
        )

        if not items:
            raise EmptySalesReturnError(
                "Sales return contains no items."
            )

        #
        # Validate all sale items and variants first.
        #
        for item in items:

            sale_item = self._sale_item_repository.get_by_id(
                item.sale_item_id,
            )

            if sale_item is None:
                raise SaleItemNotFoundError(
                    "Sale item not found."
                )

            self._product_variant_service.get_by_id(
                sale_item.product_variant_id,
            )

        try:

            #
            # Return stock.
            #
            for item in items:

                sale_item = self._sale_item_repository.get_by_id(
                    item.sale_item_id,
                )

                self._stock_movement_service.record_movement(
                    variant_id=sale_item.product_variant_id,
                    movement_type=MovementType.SALES_RETURN,
                    quantity=item.quantity,
                    reference=sales_return.return_number,
                    notes="Sales Return",
                )

            #
            # Complete the return.
            #
            sales_return.status = SalesReturnStatus.COMPLETED

            self._repository.update(
                sales_return,
            )

            #
            # Commit the complete operation once.
            #
            self._stock_movement_service.commit()

        except Exception:

            self._stock_movement_service.rollback()

            raise

    def generate_return_number(self) -> str:

        last = self._repository.get_last()
        if last is None:
            return "RET-000001"
        try:
            number = int(
                last.return_number.split("-")[1]
            )
        except (IndexError, ValueError):
            number = 0

        return f"RET-{number + 1:06d}"


  

    