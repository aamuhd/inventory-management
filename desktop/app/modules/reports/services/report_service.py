from dataclasses import dataclass
from datetime import date, datetime, time, timezone
from decimal import Decimal

from app.modules.reports.repositories.report_repository import (
    ReportRepository,
)

from app.modules.inventory.enums.movement_type import MovementType
from app.modules.inventory.models.stock_movement import StockMovement



@dataclass
class RecentSaleSummary:
    invoice: str
    customer: str
    amount: Decimal
    date: str


@dataclass
class LowStockSummary:
    product: str
    stock: int


@dataclass
class DashboardSummary:
    products: int
    customers: int
    suppliers: int
    today_sales: Decimal
    today_purchases: Decimal
    low_stock: int
    recent_sales: list[RecentSaleSummary]
    low_stock_products: list[LowStockSummary]


@dataclass
class SalesSummary:
    total_sales: Decimal
    total_items_sold: int
    number_of_sales: int
    average_sale: Decimal


@dataclass
class InventorySummary:
    total_variants: int
    total_stock_quantity: int
    inventory_cost_value: Decimal
    inventory_selling_value: Decimal
    low_stock_count: int


@dataclass
class PurchaseSummary:
    number_of_orders: int
    total_purchase_amount: Decimal
    total_items_ordered: int
    total_items_received: int


@dataclass
class SalesReturnSummary:
    number_of_returns: int
    total_return_amount: Decimal
    total_items_returned: int


@dataclass
class StockMovementSummary:
    total_movements: int
    total_purchased: int
    total_sold: int
    total_sales_returned: int
    total_damaged: int
    total_returned_to_supplier: int
    total_adjustment_in: int
    total_adjustment_out: int
    total_returned_in: int


class ReportService:

    def __init__(
        self,
        repository: ReportRepository,
    ) -> None:
        self._repository = repository

    # =========================================================
    # DATE RANGE
    # =========================================================

    def _make_start_datetime(
        self,
        start_date: date | None,
    ) -> datetime | None:

        if start_date is None:
            return None

        return datetime.combine(
            start_date,
            time.min,
            tzinfo=timezone.utc,
        )

    def _make_end_datetime(
        self,
        end_date: date | None,
    ) -> datetime | None:

        if end_date is None:
            return None

        return datetime.combine(
            end_date,
            time.max,
            tzinfo=timezone.utc,
        )

    # =========================================================
    # SALES SUMMARY
    # =========================================================

    def get_sales_summary(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> SalesSummary:

        start_datetime = self._make_start_datetime(
            start_date,
        )

        end_datetime = self._make_end_datetime(
            end_date,
        )

        sales = self._repository.get_sales(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

        total_sales = Decimal("0.00")
        total_items_sold = 0

        for sale in sales:

            total_sales += sale.total_amount

            for item in sale.items:
                total_items_sold += item.quantity

        number_of_sales = len(sales)

        if number_of_sales > 0:
            average_sale = (
                total_sales / number_of_sales
            )
        else:
            average_sale = Decimal("0.00")

        return SalesSummary(
            total_sales=total_sales,
            total_items_sold=total_items_sold,
            number_of_sales=number_of_sales,
            average_sale=average_sale,
        )

    # =========================================================
    # INVENTORY SUMMARY
    # =========================================================

    def get_inventory_summary(
        self,
    ) -> InventorySummary:

        variants = self._repository.get_inventory()

        total_stock_quantity = 0
        inventory_cost_value = Decimal("0.00")
        inventory_selling_value = Decimal("0.00")
        low_stock_count = 0

        for variant in variants:

            total_stock_quantity += (
                variant.stock_quantity
            )

            inventory_cost_value += (
                Decimal(variant.stock_quantity)
                * variant.cost_price
            )

            inventory_selling_value += (
                Decimal(variant.stock_quantity)
                * variant.selling_price
            )

            if (
                variant.stock_quantity
                <= variant.reorder_level
            ):
                low_stock_count += 1

        return InventorySummary(
            total_variants=len(variants),
            total_stock_quantity=total_stock_quantity,
            inventory_cost_value=inventory_cost_value,
            inventory_selling_value=inventory_selling_value,
            low_stock_count=low_stock_count,
        )

    # =========================================================
    # PURCHASE SUMMARY
    # =========================================================

    def get_purchase_summary(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> PurchaseSummary:

        start_datetime = self._make_start_datetime(
            start_date,
        )

        end_datetime = self._make_end_datetime(
            end_date,
        )

        purchase_orders = (
            self._repository.get_purchase_orders(
                start_datetime=start_datetime,
                end_datetime=end_datetime,
            )
        )

        total_purchase_amount = Decimal("0.00")
        total_items_ordered = 0
        total_items_received = 0

        for order in purchase_orders:

            total_purchase_amount += (
                order.total_amount
            )

            for item in order.items:

                total_items_ordered += (
                    item.quantity
                )

                total_items_received += (
                    item.received_quantity
                )

        return PurchaseSummary(
            number_of_orders=len(purchase_orders),
            total_purchase_amount=total_purchase_amount,
            total_items_ordered=total_items_ordered,
            total_items_received=total_items_received,
        )

    # =========================================================
    # SALES RETURN SUMMARY
    # =========================================================

    def get_sales_return_summary(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> SalesReturnSummary:

        start_datetime = self._make_start_datetime(
            start_date,
        )

        end_datetime = self._make_end_datetime(
            end_date,
        )

        sales_returns = (
            self._repository.get_sales_returns(
                start_datetime=start_datetime,
                end_datetime=end_datetime,
            )
        )

        total_return_amount = Decimal("0.00")
        total_items_returned = 0

        for sales_return in sales_returns:

            total_return_amount += (
                sales_return.total_amount
            )

            for item in sales_return.items:
                total_items_returned += item.quantity

        return SalesReturnSummary(
            number_of_returns=len(sales_returns),
            total_return_amount=total_return_amount,
            total_items_returned=total_items_returned,
        )

    # =========================================================
    # STOCK MOVEMENT SUMMARY
    # =========================================================

    def get_stock_movement_summary(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> StockMovementSummary:

        start_datetime = self._make_start_datetime(
            start_date,
        )

        end_datetime = self._make_end_datetime(
            end_date,
        )

        movements = self._repository.get_stock_movements(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

        total_purchased = 0
        total_sold = 0
        total_sales_returned = 0
        total_damaged = 0
        total_returned_to_supplier = 0
        total_adjustment_in = 0
        total_adjustment_out = 0
        total_returned_in = 0

        for movement in movements:

            quantity = abs(movement.quantity)

            if movement.movement_type == MovementType.PURCHASE:
                total_purchased += quantity

            elif movement.movement_type == MovementType.SALE:
                total_sold += quantity

            elif (
                movement.movement_type
                == MovementType.SALES_RETURN
            ):
                total_sales_returned += quantity

            elif movement.movement_type == MovementType.DAMAGED:
                total_damaged += quantity

            elif (
                movement.movement_type
                == MovementType.RETURN_TO_SUPPLIER
            ):
                total_returned_to_supplier += quantity

            elif (
                movement.movement_type
                == MovementType.ADJUSTMENT
            ):
                if movement.quantity > 0:
                    total_adjustment_in += quantity
                else:
                    total_adjustment_out += quantity

            elif movement.movement_type == MovementType.RETURN_IN:
                total_returned_in += quantity

        return StockMovementSummary(
            total_movements=len(movements),
            total_purchased=total_purchased,
            total_sold=total_sold,
            total_sales_returned=total_sales_returned,
            total_damaged=total_damaged,
            total_returned_to_supplier=total_returned_to_supplier,
            total_adjustment_in=total_adjustment_in,
            total_adjustment_out=total_adjustment_out,
            total_returned_in=total_returned_in,
        )

    # =========================================================
    # STOCK MOVEMENT HISTORY
    # =========================================================

    def get_stock_movement_history(
        self,
        start_date: date | None = None,
        end_date: date | None = None,
    ) -> list[StockMovement]:

        start_datetime = self._make_start_datetime(
            start_date,
        )

        end_datetime = self._make_end_datetime(
            end_date,
        )

        return self._repository.get_stock_movements(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )

    def get_dashboard_summary(self) -> DashboardSummary:

        today = date.today()

        sales = self._repository.get_sales(
            start_datetime=self._make_start_datetime(today),
            end_datetime=self._make_end_datetime(today),
        )

        purchase_orders = self._repository.get_purchase_orders(
            start_datetime=self._make_start_datetime(today),
            end_datetime=self._make_end_datetime(today),
        )

        inventory = self._repository.get_inventory()

        customers = self._repository.get_customer_count()
        suppliers = self._repository.get_supplier_count()

        today_sales = Decimal("0.00")

        for sale in sales:
            today_sales += sale.total_amount

        today_purchases = Decimal("0.00")

        for order in purchase_orders:
            today_purchases += order.total_amount

        low_stock_products = []

        for variant in inventory:

            if variant.stock_quantity <= variant.reorder_level:

                product_name = (
                    variant.product.name
                    if variant.product
                    else "Unknown"
                )

                low_stock_products.append(
                    LowStockSummary(
                        product=product_name,
                        stock=variant.stock_quantity,
                    )
                )

        recent_sales = self._repository.get_recent_sales(
            limit=10,
        )

        recent_sale_summaries = []

        for sale in recent_sales:

            customer_name = (
                sale.customer.name
                if sale.customer
                else "Walk-in Customer"
            )

            recent_sale_summaries.append(
                RecentSaleSummary(
                    invoice=sale.invoice_number,
                    customer=customer_name,
                    amount=sale.total_amount,
                    date=sale.sale_date.strftime("%Y-%m-%d"),
                )
            )

        return DashboardSummary(
            products=len(inventory),
            customers=customers,
            suppliers=suppliers,
            today_sales=today_sales,
            today_purchases=today_purchases,
            low_stock=len(low_stock_products),
            recent_sales=recent_sale_summaries,
            low_stock_products=low_stock_products,
        )