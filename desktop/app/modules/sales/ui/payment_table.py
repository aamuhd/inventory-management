from __future__ import annotations

from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.sales.models.sale_payment import SalePayment


class PaymentTable(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self._payments: list[
            SalePayment
        ] = []

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.table = QTableWidget()

        self.table.setColumnCount(
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Date",
                "Amount",
                "Payment Method",
                "Notes",
            ]
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout = QVBoxLayout(
            self
        )

        layout.addWidget(
            self.table
        )

    # =========================================================
    # LOAD
    # =========================================================

    def load(
        self,
        payments: list[SalePayment],
    ) -> None:

        self._payments = list(
            payments
        )

        self.table.setRowCount(
            len(payments)
        )

        for row, payment in enumerate(
            payments
        ):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    str(
                        payment.payment_date
                    )
                ),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    f"{payment.amount:,.2f}"
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    payment.payment_method
                ),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    payment.notes or "-"
                ),
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self._payments.clear()

        self.table.clearContents()

        self.table.setRowCount(
            0
        )
