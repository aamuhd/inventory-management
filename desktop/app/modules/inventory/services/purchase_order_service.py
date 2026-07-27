from datetime import date
from decimal import Decimal
from uuid import UUID

from app.modules.inventory.enums.purchase_order_status import (
    PurchaseOrderStatus,
)
from app.modules.inventory.exceptions import (
    EmptyPurchaseOrderError,
    InvalidPurchaseOrderStateError,
    OverReceiveError,
    PurchaseOrderItemNotFoundError,
    PurchaseOrderNotFoundError,
    DuplicatePurchaseOrderItemError,
)
from app.modules.inventory.models.purchase_order import PurchaseOrder
from app.modules.inventory.repositories.purchase_order_item_repository import (
    PurchaseOrderItemRepository,
)
from app.modules.inventory.repositories.purchase_order_repository import (
    PurchaseOrderRepository,
)
from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)
from app.modules.inventory.services.stock_movement_service import (
    StockMovementService,
)
from app.modules.inventory.services.supplier_service import (
    SupplierService,
)
from app.modules.inventory.models.purchase_order_item import PurchaseOrderItem


class PurchaseOrderService:

    def __init__(
        self,
        purchase_order_repository: PurchaseOrderRepository,
        purchase_order_item_repository: PurchaseOrderItemRepository,
        supplier_service: SupplierService,
        product_variant_service: ProductVariantService,
        stock_movement_service: StockMovementService,
    ) -> None:

        self._purchase_order_repository = purchase_order_repository
        self._purchase_order_item_repository = purchase_order_item_repository
        self._supplier_service = supplier_service
        self._product_variant_service = product_variant_service
        self._stock_movement_service = stock_movement_service

    def create(
        self,
        supplier_id: UUID,
        order_number: str,
        order_date: date,
        expected_date: date | None = None,
        notes: str | None = None,
    ) -> PurchaseOrder:

        self._supplier_service.get_by_id(
            supplier_id,
        )

        purchase_order = PurchaseOrder(
            supplier_id=supplier_id,
            order_number=order_number,
            order_date=order_date,
            expected_date=expected_date,
            notes=notes,
            status=PurchaseOrderStatus.DRAFT,
            total_amount=Decimal("0.00"),
        )

        return self._purchase_order_repository.create(
            purchase_order,
        )

    def get_by_id(
        self,
        purchase_order_id: UUID,
    ) -> PurchaseOrder:

        purchase_order = (
            self._purchase_order_repository.get_by_id(
                purchase_order_id,
            )
        )

        if purchase_order is None:
            raise PurchaseOrderNotFoundError(
                "Purchase order not found."
            )

        return purchase_order

    def get_all(
        self,
    ) -> list[PurchaseOrder]:

        return self._purchase_order_repository.get_all()

    def delete(
        self,
        purchase_order_id: UUID,
    ) -> None:

        purchase_order = self.get_by_id(
            purchase_order_id,
        )

        if purchase_order.status != PurchaseOrderStatus.DRAFT:
            raise InvalidPurchaseOrderStateError(
                "Only draft purchase orders can be deleted."
            )

        self._purchase_order_repository.delete(
            purchase_order,
        )

    def add_item(
        self,
        purchase_order_id: UUID,
        variant_id: UUID,
        quantity: int,
        unit_cost: Decimal,
    ) -> PurchaseOrderItem:

        purchase_order = self.get_by_id(
            purchase_order_id,
        )

        if purchase_order.status != PurchaseOrderStatus.DRAFT:
            raise InvalidPurchaseOrderStateError(
                "Only draft purchase orders can be modified."
            )

        self._product_variant_service.get_by_id(
            variant_id,
        )

        existing_item = (
            self._purchase_order_item_repository.get_by_purchase_order_and_variant(
                purchase_order_id,
                variant_id,
            )
        )

        if existing_item is not None:
            raise DuplicatePurchaseOrderItemError(
                "Variant already exists in this purchase order."
            )

        item = PurchaseOrderItem(
            purchase_order_id=purchase_order_id,
            product_variant_id=variant_id,
            quantity=quantity,
            unit_cost=unit_cost,
        )

        item = self._purchase_order_item_repository.create(
            item,
        )

        self._recalculate_total(
            purchase_order_id,
        )

        return item
    
    def _recalculate_total(
        self,
        purchase_order_id: UUID,
    ) -> None:

        purchase_order = self.get_by_id(
            purchase_order_id,
        )

        items = (
            self._purchase_order_item_repository.get_by_purchase_order(
                purchase_order_id,
            )
        )

        total = Decimal("0.00")

        for item in items:
            total += item.quantity * item.unit_cost

        purchase_order.total_amount = total

        self._purchase_order_repository.update(
            purchase_order,
        )

    def submit(
        self,
        purchase_order_id: UUID,
    ) -> None:

        purchase_order = self.get_by_id(
            purchase_order_id,
        )

        if purchase_order.status != PurchaseOrderStatus.DRAFT:
            raise InvalidPurchaseOrderStateError(
                "Purchase order has already been submitted."
            )

        items = self._purchase_order_item_repository.get_by_purchase_order(
            purchase_order_id,
        )

        if not items:
            raise EmptyPurchaseOrderError(
                "Purchase order contains no items."
            )

        purchase_order.status = PurchaseOrderStatus.ORDERED

        self._purchase_order_repository.update(
            purchase_order,
        )


    def receive_item(
        self,
        item_id: UUID,
        quantity: int,
    ) -> None:

        item = self._purchase_order_item_repository.get_by_id(
            item_id,
        )

        if item is None:
            raise PurchaseOrderItemNotFoundError(
                "Purchase order item not found."
            )

        purchase_order = self.get_by_id(
            item.purchase_order_id,
        )

        if purchase_order.status not in (
            PurchaseOrderStatus.ORDERED,
            PurchaseOrderStatus.PARTIALLY_RECEIVED,
        ):
            raise InvalidPurchaseOrderStateError(
                "Purchase order cannot receive goods."
            )

        outstanding = item.quantity - item.received_quantity

        if quantity > outstanding:
            raise OverReceiveError(
                "Cannot receive more than ordered."
            )

        self._stock_movement_service.purchase_stock(
            variant_id=item.product_variant_id,
            quantity=quantity,
            reference=purchase_order.order_number,
            notes="Purchase Order Receipt",
        )

        item.received_quantity += quantity

        self._purchase_order_item_repository.update(
            item,
        )

        self._update_purchase_order_status(
            purchase_order.id,
        )

    def _update_purchase_order_status(
        self,
        purchase_order_id: UUID,
    ) -> None:

        purchase_order = self.get_by_id(
            purchase_order_id,
        )

        items = (
            self._purchase_order_item_repository.get_by_purchase_order(
                purchase_order_id,
            )
        )

        if all(
            item.received_quantity == item.quantity
            for item in items
        ):
            purchase_order.status = PurchaseOrderStatus.RECEIVED

        elif any(
            item.received_quantity > 0
            for item in items
        ):
            purchase_order.status = (
                PurchaseOrderStatus.PARTIALLY_RECEIVED
            )

        self._purchase_order_repository.update(
            purchase_order,
        )

    def get_item(
        self,
        item_id: UUID,
    ) -> PurchaseOrderItem:

        item = self._purchase_order_item_repository.get_by_id(
            item_id,
        )

        if item is None:
            raise PurchaseOrderItemNotFoundError(
                "Purchase order item not found."
            )

        return item