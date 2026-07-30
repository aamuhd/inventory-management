from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from app.modules.inventory.models.supplier_return import SupplierReturn


class SupplierReturnTable(QTableWidget):

    supplier_return_selected = Signal(SupplierReturn)

    HEADERS = [
        "Return Number",
        "Supplier",
        "Purchase Order",
        "Date",
        "Status",
    ]

    def __init__(self):

        super().__init__()

        self._supplier_returns: list[SupplierReturn] = []

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
        supplier_returns: list[SupplierReturn],
    ):

        self._supplier_returns = supplier_returns

        self.setRowCount(
            len(supplier_returns),
        )

        for row, supplier_return in enumerate(
            supplier_returns,
        ):

            purchase_order = ""

            if supplier_return.purchase_order:

                purchase_order = (
                    supplier_return.purchase_order.order_number
                )

            self.setItem(
                row,
                0,
                QTableWidgetItem(
                    supplier_return.return_number,
                ),
            )

            self.setItem(
                row,
                1,
                QTableWidgetItem(
                    supplier_return.supplier.name,
                ),
            )

            self.setItem(
                row,
                2,
                QTableWidgetItem(
                    purchase_order,
                ),
            )

            self.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(
                        supplier_return.return_date,
                    ),
                ),
            )

            self.setItem(
                row,
                4,
                QTableWidgetItem(
                    supplier_return.status.value,
                ),
            )

    def clear_table(self):

        self._supplier_returns.clear()

        self.setRowCount(
            0,
        )

    def _on_selection_changed(self):

        row = self.currentRow()

        if row < 0:
            return

        self.supplier_return_selected.emit(
            self._supplier_returns[row],
        )