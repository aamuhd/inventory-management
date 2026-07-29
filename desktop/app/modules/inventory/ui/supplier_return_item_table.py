from decimal import Decimal

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from app.modules.inventory.models.supplier_return_item import SupplierReturnItem


class SupplierReturnItemTable(QTableWidget):

    item_selected = Signal(SupplierReturnItem)

    HEADERS = [
        "Variant",
        "Quantity",
        "Reason",
        "Unit Cost",
        "Subtotal",
    ]

    def __init__(self):

        super().__init__()

        self._items: list[SupplierReturnItem] = []

        self._configure_table()

        self.itemSelectionChanged.connect(
            self._on_selection_changed,
        )

    def _configure_table(self):

        self.setColumnCount(
            len(self.HEADERS),
        )

        self.setHorizontalHeaderLabels(
            self.HEADERS,
        )

        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch,
        )

        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows,
        )

        self.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection,
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers,
        )

        self.setAlternatingRowColors(
            True,
        )

    def load(
        self,
        items: list[SupplierReturnItem],
    ):

        self._items = items

        self.setRowCount(
            len(items),
        )

        for row, item in enumerate(items):

            variant = ""

            if item.product_variant:

                if item.product_variant.sku:
                    variant = item.product_variant.sku
                else:
                    variant = str(
                        item.product_variant.length,
                    )

            subtotal = (
                Decimal(item.quantity)
                * item.product_variant.cost_price
            )

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
                    item.reason or "",
                ),
            )

            self.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(item.product_variant.cost_price),
                ),
            )

            self.setItem(
                row,
                4,
                QTableWidgetItem(
                    str(subtotal),
                ),
            )

    def clear_table(self):

        self._items.clear()

        self.setRowCount(
            0,
        )

    def _on_selection_changed(self):

        row = self.currentRow()

        if row < 0:
            return

        self.item_selected.emit(
            self._items[row],
        )