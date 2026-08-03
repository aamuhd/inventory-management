from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.sales.models.sale import Sale


class SaleTable(QWidget):

    sale_selected = Signal(Sale)

    def __init__(self):
        super().__init__()

        self._sales: list[Sale] = []

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):

        self.table = QTableWidget()

        self.table.setColumnCount(6)

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
        sales: list[Sale],
    ):

        self._sales = list(sales)

        self.table.setRowCount(
            len(sales),
        )

        for row, sale in enumerate(sales):

            customer = (
                sale.customer.name
                if sale.customer is not None
                else "Walk-in Customer"
            )

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    sale.invoice_number,
                ),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    customer,
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(sale.sale_date),
                ),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    sale.status.value,
                ),
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    str(sale.total_amount),
                ),
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(
                    str(len(sale.items)),
                ),
            )

    def _emit_selected(self):

        row = self.table.currentRow()

        print("Current row:", row)
        print("Sales:", self._sales)

        if row < 0:
            return

        print("Emitting:", self._sales[row])

        self.sale_selected.emit(
            self._sales[row],
        )

    def selected_sale(
        self,
    ) -> Sale | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        return self._sales[row]

    def clear(self):

        self.table.clearContents()
        self.table.setRowCount(0)
        self._sales = []