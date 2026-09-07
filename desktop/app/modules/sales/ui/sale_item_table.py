from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.sales.models.sale_item import SaleItem


class SaleItemTable(QWidget):

    item_selected = Signal(SaleItem)

    def __init__(self):
        super().__init__()

        self._items: list[SaleItem] = []

        self._build_ui()
        self._connect_signals()

    def _build_ui(self):

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(
            [
                "Product",
                "Quantity",
                "Unit Price",
                "Subtotal",
                "Length",
            ]
        )

        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch,
        )

        layout = QVBoxLayout(self)

        layout.addWidget(self.table)

    def _connect_signals(self):

        self.table.itemSelectionChanged.connect(
            self._emit_selected,
        )

    def load(
        self,
        items: list[SaleItem],
    ) -> None:

        self._items = list(items)

        self.table.setRowCount(len(self._items))
        """
        self._items = list(items)
        self.table.setRowCount(len(self._items))
        """

        for row, item in enumerate(items):

            variant = item.product_variant

            subtotal = (
                item.quantity * item.unit_price
            )

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    variant.product.name,
                ),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    str(item.quantity),
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(item.unit_price),
                ),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(subtotal),
                ),
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    f"{variant.length} yards",
                ),
            )

    def _emit_selected(self):

        row = self.table.currentRow()

        if row < 0:
            return

        self.item_selected.emit(
            self._items[row],
        )

    def selected_item(
        self,
    ) -> SaleItem | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        return self._items[row]

    def clear(self):

        self.table.clearContents()
        self.table.setRowCount(0)
        self._items = []