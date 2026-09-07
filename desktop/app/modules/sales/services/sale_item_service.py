from uuid import UUID

from app.modules.sales.dtos.returnable_sale_item import ReturnableSaleItem
from app.modules.sales.exceptions import SaleItemNotFoundError
from app.modules.sales.models.sale_item import SaleItem
from app.modules.sales.repositories.sale_item_repository import SaleItemRepository
from app.modules.sales.repositories.sales_return_item_repository import SalesReturnItemRepository


class SaleItemService:

    def __init__(
        self,
        repository: SaleItemRepository,
        sales_return_item_repository: SalesReturnItemRepository,
    ):
        self._repository = repository
        self._sales_return_item_repository = (
            sales_return_item_repository
        )

    def get_by_id(
        self,
        sale_item_id: UUID,
    ) -> SaleItem:

        item = self._repository.get_by_id(
            sale_item_id,
        )

        if item is None:
            raise SaleItemNotFoundError(
                "Sale item not found."
            )

        return item

    def get_by_sale(
        self,
        sale_id: UUID,
    ) -> list[SaleItem]:

        return self._repository.get_by_sale(
            sale_id,
        )

    def get_returnable_items(
        self,
        sale_id: UUID,
    ) -> list[ReturnableSaleItem]:

        sale_items = self.get_by_sale(sale_id)

        result: list[ReturnableSaleItem] = []

        for sale_item in sale_items:

            returned_items = (
                self._sales_return_item_repository.get_by_sale_item(
                    sale_item.id,
                )
            )

            returned_quantity = sum(
                (
                    item.quantity
                    for item in returned_items
                ),
                start=0,
            )

            available_quantity = (
                sale_item.quantity - returned_quantity
            )

            if available_quantity <= 0:
                continue

            result.append(
                ReturnableSaleItem(
                    sale_item=sale_item,
                    sold_quantity=sale_item.quantity,
                    returned_quantity=returned_quantity,
                    available_quantity=available_quantity,
                )
            )

        return result