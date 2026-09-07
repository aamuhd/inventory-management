from sqlalchemy.orm import selectinload
from uuid import UUID

from sqlmodel import Session, select, desc

from app.modules.base_repo import BaseRepository
from app.modules.sales.models.sales_return import SalesReturn

from app.modules.sales.models.sale import Sale
from app.modules.sales.models.sales_return_item import SalesReturnItem
from app.modules.inventory.models.product_variant import ProductVariant
from app.modules.sales.models.sale_item import SaleItem



class SalesReturnRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ):
        super().__init__(session)

    def create(
        self,
        sales_return: SalesReturn,
    ) -> SalesReturn:

        self._session.add(sales_return)
        self._commit()
        self._session.refresh(sales_return)

        return sales_return

    def get_all(
        self,
    ) -> list[SalesReturn]:

        statement = (
            select(SalesReturn)
            .options(
                selectinload(SalesReturn.sale)
                .selectinload(Sale.customer),
            )
            .order_by(
                desc(SalesReturn.return_date),
            )
        )

        return list(
            self._session.exec(statement)
        )

    def get_by_id(
        self,
        sales_return_id: UUID,
    ) -> SalesReturn | None:

        statement = (
            select(SalesReturn)
            .where(
                SalesReturn.id == sales_return_id,
            )
            .options(
                selectinload(SalesReturn.sale)
                .selectinload(Sale.customer),

                selectinload(SalesReturn.items)
                .selectinload(SalesReturnItem.sale_item)
                .selectinload(SaleItem.product_variant)
                .selectinload(ProductVariant.product),
            )
        )

        return self._session.exec(
            statement,
        ).first()

    def update(
        self,
        sales_return: SalesReturn,
    ) -> SalesReturn:

        self._session.add(sales_return)
        self._commit()
        self._session.refresh(sales_return)

        return sales_return

    def delete(
        self,
        sales_return: SalesReturn,
    ) -> None:

        self._session.delete(sales_return)
        self._commit()

    def get_by_sale(
        self,
        sale_id: UUID,
    ) -> list[SalesReturn]:

        statement = (
            select(SalesReturn)
            .where(
                SalesReturn.sale_id == sale_id,
            )
            .order_by(
                desc(SalesReturn.return_date),
            )
        )

        return list(
            self._session.exec(statement),
        )

    def get_last(self) -> SalesReturn | None:

        statement = (
            select(SalesReturn)
            .order_by(desc(SalesReturn.created_at))
            .limit(1)
        )

        return self._session.exec(statement).first()