from datetime import date
from uuid import UUID

from sqlmodel import Session, select
from sqlalchemy import desc

from app.modules.base_repo import BaseRepository
from app.modules.sales.models.sale_payment import SalePayment


class SalePaymentRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session)

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self,
        payment: SalePayment,
    ) -> SalePayment:

        self._session.add(payment)
        self._commit()
        self._session.refresh(payment)

        return payment

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        payment: SalePayment,
    ) -> SalePayment:

        self._session.add(payment)
        self._session.flush()
        self._session.refresh(payment)

        return payment

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        payment: SalePayment,
    ) -> None:

        self._session.delete(payment)
        self._commit()

    # =========================================================
    # GET BY ID
    # =========================================================

    def get_by_id(
        self,
        payment_id: UUID,
    ) -> SalePayment | None:

        return self._session.get(
            SalePayment,
            payment_id,
        )

    # =========================================================
    # GET BY SALE
    # =========================================================

    def get_by_sale(
        self,
        sale_id: UUID,
    ) -> list[SalePayment]:

        statement = (
            select(SalePayment)
            .where(
                SalePayment.sale_id == sale_id
            )
            .order_by(
                desc(SalePayment.payment_date)
            )
        )

        return list(
            self._session.exec(statement)
        )

    # =========================================================
    # GET TOTAL PAID
    # =========================================================

    def get_total_paid(
        self,
        sale_id: UUID,
    ) -> object:

        payments = self.get_by_sale(
            sale_id
        )

        total = 0

        for payment in payments:
            total += payment.amount

        return total
