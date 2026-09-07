from __future__ import annotations

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.sales.models.sale import Sale


class SaleTable(QWidget):

    sale_selected = Signal(Sale)

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName(
            "saleTableContainer"
        )

        self._sales: list[Sale] = []

        self._build_ui()
        self._connect_signals()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.table = QTableWidget()

        self.table.setObjectName(
            "saleTable"
        )

        self.table.setColumnCount(
            6
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Invoice",
                "Customer",
                "Date",
                "Status",
                "Total",
                "Items",
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.table.setSortingEnabled(
            True
        )

        layout = QVBoxLayout(
            self
        )

        layout.addWidget(
            self.table
        )

    # =========================================================
    # SIGNALS
    # =========================================================

    def _connect_signals(self) -> None:

        self.table.itemSelectionChanged.connect(
            self._emit_selected
        )

    # =========================================================
    # LOAD
    # =========================================================

    def load(
        self,
        sales: list[Sale],
    ) -> None:

        self._sales = list(
            sales
        )

        self.table.setRowCount(
            len(sales)
        )

        for row, sale in enumerate(
            sales
        ):

            customer = (
                sale.customer.name
                if sale.customer is not None
                else "Walk-in Customer"
            )

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    sale.invoice_number
                ),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    customer
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(
                        sale.sale_date
                    )
                ),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    sale.status.value
                ),
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    str(
                        sale.total_amount
                    )
                ),
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(
                    str(
                        len(
                            sale.items
                        )
                    )
                ),
            )

    # =========================================================
    # SELECTION
    # =========================================================

    def selected_sale(
        self,
    ) -> Sale | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        if row >= len(
            self._sales
        ):
            return None

        return self._sales[row]

    def _emit_selected(self) -> None:

        sale = self.selected_sale()

        if sale is None:
            return

        self.sale_selected.emit(
            sale
        )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self.table.clearContents()

        self.table.setRowCount(
            0
        )

        self._sales.clear()