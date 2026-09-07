from datetime import datetime

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, col, func

from app.modules.base_repo import BaseRepository

from app.modules.inventory.models.product_variant import ProductVariant
from app.modules.inventory.models.purchase_order import PurchaseOrder
from app.modules.inventory.models.purchase_order_item import PurchaseOrderItem
from app.modules.inventory.models.stock_movement import StockMovement

from app.modules.sales.enums.sale_status import SaleStatus
from app.modules.sales.models.sale import Sale
from app.modules.sales.models.sale_item import SaleItem
from app.modules.sales.models.sales_return import SalesReturn
from app.modules.sales.models.sales_return_item import SalesReturnItem

from app.modules.sales.enums.sales_return_status import SalesReturnStatus

from app.modules.sales.models.customer import Customer
from app.modules.inventory.models.supplier import Supplier


class ReportRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session)

    # ---------------------------------------------------------
    # SALES
    # ---------------------------------------------------------

    def get_sales(
        self,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[Sale]:

        statement = (
            select(Sale)
            .options(
                selectinload(Sale.customer),

                selectinload(Sale.items)
                .selectinload(SaleItem.product_variant)
                .selectinload(ProductVariant.product),
            )
            .where(
                Sale.status == SaleStatus.COMPLETED,
            )
            .order_by(
                col(Sale.sale_date).desc(),
            )
        )

        # Sale uses a date field, so filtering is handled
        # separately from StockMovement's datetime field.

        if start_datetime is not None:
            statement = statement.where(
                Sale.sale_date >= start_datetime.date(),
            )

        if end_datetime is not None:
            statement = statement.where(
                Sale.sale_date <= end_datetime.date(),
            )

        return list(
            self._session.exec(statement)
        )

    # ---------------------------------------------------------
    # SALES RETURNS
    # ---------------------------------------------------------

    def get_sales_returns(
        self,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[SalesReturn]:

        statement = (
            select(SalesReturn)
            .options(
                selectinload(SalesReturn.sale)
                .selectinload(Sale.customer),

                selectinload(SalesReturn.items)
                .selectinload(SalesReturnItem.sale_item)
                .selectinload(SaleItem.product_variant)
                .selectinload(ProductVariant.product),
            )
            .where(
                SalesReturn.status == SalesReturnStatus.COMPLETED,
            )
            .order_by(
                col(SalesReturn.return_date).desc(),
            )
        )

        if start_datetime is not None:
            statement = statement.where(
                SalesReturn.return_date
                >= start_datetime.date(),
            )

        if end_datetime is not None:
            statement = statement.where(
                SalesReturn.return_date
                <= end_datetime.date(),
            )

        return list(
            self._session.exec(statement)
        )

    # ---------------------------------------------------------
    # PURCHASE ORDERS
    # ---------------------------------------------------------

    def get_purchase_orders(
        self,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[PurchaseOrder]:

        statement = (
            select(PurchaseOrder)
            .options(
                selectinload(PurchaseOrder.supplier),

                selectinload(PurchaseOrder.items)
                .selectinload(
                    PurchaseOrderItem.product_variant
                )
                .selectinload(ProductVariant.product),
            )
            .order_by(
                col(PurchaseOrder.order_date).desc(),
            )
        )

        if start_datetime is not None:
            statement = statement.where(
                PurchaseOrder.order_date
                >= start_datetime.date(),
            )

        if end_datetime is not None:
            statement = statement.where(
                PurchaseOrder.order_date
                <= end_datetime.date(),
            )

        return list(
            self._session.exec(statement)
        )

    # ---------------------------------------------------------
    # STOCK MOVEMENTS
    # ---------------------------------------------------------

    def get_stock_movements(
        self,
        start_datetime: datetime | None = None,
        end_datetime: datetime | None = None,
    ) -> list[StockMovement]:

        statement = (
            select(StockMovement)
            .options(
                selectinload(StockMovement.variant)
                .selectinload(ProductVariant.product),
            )
            .order_by(
                col(StockMovement.created_at).desc(),
            )
        )

        if start_datetime is not None:
            statement = statement.where(
                StockMovement.created_at
                >= start_datetime,
            )

        if end_datetime is not None:
            statement = statement.where(
                StockMovement.created_at
                <= end_datetime,
            )

        return list(
            self._session.exec(statement)
        )

    # ---------------------------------------------------------
    # CURRENT INVENTORY
    # ---------------------------------------------------------

    def get_inventory(
        self,
    ) -> list[ProductVariant]:

        statement = (
            select(ProductVariant)
            .options(
                selectinload(ProductVariant.product),
            )
            .order_by(
                col(ProductVariant.stock_quantity).asc(),
            )
        )

        return list(
            self._session.exec(statement)
        )

    def get_recent_sales(
        self,
        limit: int = 10,
    ) -> list[Sale]:

        statement = (
            select(Sale)
            .options(
                selectinload(Sale.customer),

                selectinload(Sale.items)
                .selectinload(SaleItem.product_variant)
                .selectinload(ProductVariant.product),
            )
            .where(
                Sale.status == SaleStatus.COMPLETED,
            )
            .order_by(
                col(Sale.sale_date).desc(),
            )
            .limit(limit)
        )

        return list(
            self._session.exec(statement)
        )

    def get_customer_count(self) -> int:

        statement = select(
            func.count(col(Customer.id))
        )

        return self._session.exec(
            statement
        ).one()

    def get_supplier_count(self) -> int:

        statement = select(
            func.count(col(Supplier.id))
        )

        return self._session.exec(
            statement
        ).one()