from uuid import UUID

from sqlmodel import Session, select, desc

from app.modules.sales.models.sale import Sale
from app.modules.base_repo import BaseRepository


class SaleRepository(BaseRepository):

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
        sale: Sale,
    ) -> Sale:

        self._session.add(sale)
        self._commit()
        self._session.refresh(sale)

        return sale

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        sale: Sale,
    ) -> Sale:

        self._session.add(sale)
        self._session.flush()
        self._session.refresh(sale)

        return sale

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        sale: Sale,
    ) -> None:

        self._session.delete(sale)
        self._commit()

    # =========================================================
    # GET BY ID
    # =========================================================

    def get_by_id(
        self,
        sale_id: UUID,
    ) -> Sale | None:

        return self._session.get(
            Sale,
            sale_id,
        )

    # =========================================================
    # GET ALL
    # =========================================================

    def get_all(
        self,
    ) -> list[Sale]:

        statement = (
            select(Sale)
            .order_by(
                desc(Sale.sale_date)
            )
        )

        return list(
            self._session.exec(statement)
        )

    # =========================================================
    # GET BY CUSTOMER
    # =========================================================

    def get_by_customer(
        self,
        customer_id: UUID,
    ) -> list[Sale]:

        statement = (
            select(Sale)
            .where(
                Sale.customer_id == customer_id
            )
        )

        return list(
            self._session.exec(statement)
        )

    # =========================================================
    # GET BY INVOICE NUMBER
    # =========================================================

    def get_by_invoice_number(
        self,
        invoice_number: str,
    ) -> Sale | None:

        statement = (
            select(Sale)
            .where(
                Sale.invoice_number == invoice_number
            )
        )

        return self._session.exec(
            statement
        ).first()

    # =========================================================
    # GENERATE NEXT INVOICE NUMBER
    # =========================================================

    def generate_next_invoice_number(
        self,
        prefix: str,
    ) -> str:
        """
        Generate the next invoice number for the
        supplied prefix.

        Example:

            INV
            INV-00001
            INV-00002

        The prefix is normalized so both:

            INV
            INV-

        produce:

            INV-00001
        """

        prefix = prefix.strip().upper()

        if not prefix:
            prefix = "INV"

        normalized_prefix = prefix.rstrip("-") + "-"

        statement = select(
            Sale.invoice_number
        )

        invoice_numbers = self._session.exec(
            statement
        ).all()

        highest_number = 0

        for invoice_number in invoice_numbers:

            if not invoice_number:
                continue

            invoice_number = invoice_number.strip()

            if not invoice_number.upper().startswith(
                normalized_prefix
            ):
                continue

            suffix = invoice_number[
                len(normalized_prefix):
            ]

            if not suffix.isdigit():
                continue

            number = int(suffix)

            if number > highest_number:
                highest_number = number

        next_number = highest_number + 1

        return (
            f"{normalized_prefix}"
            f"{next_number:05d}"
        )