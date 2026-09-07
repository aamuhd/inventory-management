from datetime import date
from decimal import Decimal
from uuid import UUID

from app.modules.sales.enums.sale_status import SaleStatus
from app.modules.sales.exceptions import (
    InvalidPaymentAmountError,
    PaymentExceedsBalanceError,
    PaymentNotFoundError,
    PaymentSaleStateError,
)
from app.modules.sales.models.sale_payment import SalePayment
from app.modules.sales.repositories.sale_payment_repository import (
    SalePaymentRepository,
)
from app.modules.sales.services.sale_service import SaleService


class PaymentService:

    def __init__(
        self,
        repository: SalePaymentRepository,
        sale_service: SaleService,
    ) -> None:

        self._repository = repository
        self._sale_service = sale_service

    # =========================================================
    # CREATE PAYMENT
    # =========================================================

    def create(
        self,
        sale_id: UUID,
        amount: Decimal,
        payment_date: date,
        payment_method: str = "Cash",
        notes: str | None = None,
    ) -> SalePayment:

        sale = self._sale_service.get_by_id(
            sale_id
        )

        if sale.status != SaleStatus.COMPLETED:
            raise PaymentSaleStateError(
                "Payments can only be added to completed sales."
            )

        amount = Decimal(
            str(amount)
        ).quantize(
            Decimal("0.01")
        )

        if amount <= Decimal("0.00"):
            raise InvalidPaymentAmountError(
                "Payment amount must be greater than zero."
            )

        outstanding = self.get_balance(
            sale_id
        )

        if amount > outstanding:
            raise PaymentExceedsBalanceError(
                f"Payment exceeds the outstanding balance "
                f"of {outstanding:,.2f}."
            )

        payment = SalePayment(
            sale_id=sale_id,
            amount=amount,
            payment_date=payment_date,
            payment_method=(
                payment_method.strip()
                or "Cash"
            ),
            notes=notes,
        )

        return self._repository.create(
            payment
        )

    # =========================================================
    # GET BY ID
    # =========================================================

    def get_by_id(
        self,
        payment_id: UUID,
    ) -> SalePayment:

        payment = self._repository.get_by_id(
            payment_id
        )

        if payment is None:
            raise PaymentNotFoundError(
                "Payment not found."
            )

        return payment

    # =========================================================
    # GET BY SALE
    # =========================================================

    def get_by_sale(
        self,
        sale_id: UUID,
    ) -> list[SalePayment]:

        self._sale_service.get_by_id(
            sale_id
        )

        return self._repository.get_by_sale(
            sale_id
        )

    # =========================================================
    # TOTAL PAID
    # =========================================================

    def get_total_paid(
        self,
        sale_id: UUID,
    ) -> Decimal:

        payments = self.get_by_sale(
            sale_id
        )

        total = Decimal("0.00")

        for payment in payments:
            total += payment.amount

        return total

    # =========================================================
    # BALANCE
    # =========================================================

    def get_balance(
        self,
        sale_id: UUID,
    ) -> Decimal:

        sale = self._sale_service.get_by_id(
            sale_id
        )

        paid = self.get_total_paid(
            sale_id
        )

        balance = (
            sale.total_amount - paid
        )

        if balance < Decimal("0.00"):
            return Decimal("0.00")

        return balance
