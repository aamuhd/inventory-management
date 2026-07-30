from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
)

from app.modules.inventory.models.purchase_order import PurchaseOrder


class PurchaseOrderTable(QTableWidget):

    purchase_order_selected = Signal(PurchaseOrder)

    def __init__(self):

        super().__init__()

        self._orders = []

        self.setColumnCount(4)

        self.setHorizontalHeaderLabels(
            [
                "Order Number",
                "Supplier",
                "Date",
                "Status",
            ]
        )

        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows,
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers,
        )

        self.itemSelectionChanged.connect(
            self._emit_selection,
        )

    def load(
        self,
        orders: list[PurchaseOrder],
    ):

        self._orders = orders

        self.setRowCount(
            len(orders),
        )

        for row, order in enumerate(orders):

            supplier = (
                order.supplier.name
                if order.supplier
                else ""
            )

            self.setItem(
                row,
                0,
                QTableWidgetItem(
                    order.order_number,
                ),
            )

            self.setItem(
                row,
                1,
                QTableWidgetItem(
                    supplier,
                ),
            )

            self.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(order.order_date),
                ),
            )

            self.setItem(
                row,
                3,
                QTableWidgetItem(
                    order.status.value,
                ),
            )

    def _emit_selection(self):

        row = self.currentRow()

        if row < 0:
            return

        self.purchase_order_selected.emit(
            self._orders[row],
        )