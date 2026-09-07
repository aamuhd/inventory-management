from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.sales.models.sales_return import SalesReturn


class SalesReturnTable(QWidget):

    sales_return_selected = Signal(SalesReturn)

    def __init__(self):
        super().__init__()

        self._returns: list[SalesReturn] = []

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):

        self.table = QTableWidget()

        self.table.setColumnCount(6)

        self.table.setHorizontalHeaderLabels(
            [
                "Return No",
                "Invoice",
                "Customer",
                "Date",
                "Status",
                "Total",
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch,
        )

        layout = QVBoxLayout(self)

        layout.addWidget(
            self.table,
        )

    def _connect_signals(self):

        self.table.itemSelectionChanged.connect(
            self._emit_selected,
        )

    def load(
        self,
        returns: list[SalesReturn],
    ):

        self._returns = returns

        self.table.setRowCount(
            len(returns),
        )

        for row, sales_return in enumerate(returns):

            sale = sales_return.sale

            customer = (
                sale.customer.name
                if sale.customer is not None
                else "Walk-in Customer"
            )

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    sales_return.return_number,
                ),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    sale.invoice_number,
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    customer,
                ),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(
                        sales_return.return_date,
                    ),
                ),
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    sales_return.status.value,
                ),
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(
                    str(
                        sales_return.total_amount,
                    ),
                ),
            )

    def _emit_selected(self):

        row = self.table.currentRow()

        if row < 0:
            return

        self.sales_return_selected.emit(
            self._returns[row],
        )

    def selected_return(
        self,
    ) -> SalesReturn | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        return self._returns[row]

    def select_return(
        self,
        sales_return_id,
    ):

        for row, sales_return in enumerate(
            self._returns,
        ):

            if sales_return.id == sales_return_id:

                self.table.selectRow(
                    row,
                )

                return

    def clear(self):

        self.table.clearContents()
        self.table.setRowCount(0)
        self._returns.clear()