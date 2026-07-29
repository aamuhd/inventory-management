from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableWidget,
    QTableWidgetItem,
)
from PySide6.QtWidgets import QAbstractItemView

from app.modules.inventory.models.purchase_order_item import PurchaseOrderItem


class PurchaseOrderItemTable(QTableWidget):

    item_selected = Signal(PurchaseOrderItem)

    def __init__(self):
        super().__init__()

        self._items: list[PurchaseOrderItem] = []

        self.setColumnCount(4)

        self.setHorizontalHeaderLabels(
            [
                "Variant",
                "Quantity",
                "Cost Price",
                "Subtotal",
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
        items: list[PurchaseOrderItem],
    ):

        self._items = items

        self.setRowCount(
            len(items),
        )

        for row, item in enumerate(items):

            variant = (
                item.product_variant.sku
                if item.product_variant and item.product_variant.sku
                else str(item.product_variant.length)
                if item.product_variant
                else ""
            )

            subtotal = item.quantity * item.unit_cost

            self.setItem(
                row,
                0,
                QTableWidgetItem(
                    variant,
                ),
            )

            self.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(item.quantity),
                ),
            )

            self.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(item.unit_cost),
                ),
            )

            self.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(subtotal),
                ),
            )

    def clear(self):

        self._items.clear()
        self.setRowCount(0)

    def _emit_selection(self):

        row = self.currentRow()

        if row < 0:
            return

        self.item_selected.emit(
            self._items[row],
        )