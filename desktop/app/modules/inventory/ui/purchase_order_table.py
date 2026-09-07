from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from app.modules.inventory.models.purchase_order import PurchaseOrder


class PurchaseOrderTable(QTableWidget):

    purchase_order_selected = Signal(PurchaseOrder)

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName(
            "purchaseOrderTable"
        )

        self._orders: list[PurchaseOrder] = []

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        # -----------------------------------------------------
        # Columns
        # -----------------------------------------------------

        self.setColumnCount(4)

        self.setHorizontalHeaderLabels(
            [
                "Order Number",
                "Supplier",
                "Date",
                "Status",
            ]
        )

        # -----------------------------------------------------
        # Selection
        # -----------------------------------------------------

        self.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # -----------------------------------------------------
        # Appearance
        # -----------------------------------------------------

        self.setAlternatingRowColors(True)

        self.verticalHeader().setVisible(False)

        self.setWordWrap(False)

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # -----------------------------------------------------
        # Sorting
        # -----------------------------------------------------

        self.setSortingEnabled(True)

        # -----------------------------------------------------
        # Responsive columns
        # -----------------------------------------------------

        header = self.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        header.setMinimumSectionSize(100)

        # -----------------------------------------------------
        # Selection event
        # -----------------------------------------------------

        self.itemSelectionChanged.connect(
            self._emit_selection
        )

    # =========================================================
    # DATA
    # =========================================================

    def load(
        self,
        orders: list[PurchaseOrder],
    ) -> None:

        self._orders = orders

        # Temporarily disable sorting while
        # populating the table.
        sorting_enabled = (
            self.isSortingEnabled()
        )

        self.setSortingEnabled(False)

        self.setRowCount(
            len(orders)
        )

        for row, order in enumerate(
            orders
        ):

            # -------------------------------------------------
            # Order Number
            # -------------------------------------------------

            order_number_item = QTableWidgetItem(
                order.order_number
            )

            self.setItem(
                row,
                0,
                order_number_item,
            )

            # -------------------------------------------------
            # Supplier
            # -------------------------------------------------

            supplier_name = ""

            if order.supplier is not None:

                supplier_name = (
                    order.supplier.name
                )

            self.setItem(
                row,
                1,
                QTableWidgetItem(
                    supplier_name
                ),
            )

            # -------------------------------------------------
            # Date
            # -------------------------------------------------

            self.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(order.order_date)
                ),
            )

            # -------------------------------------------------
            # Status
            # -------------------------------------------------

            self.setItem(
                row,
                3,
                QTableWidgetItem(
                    order.status.value
                ),
            )

        self.setSortingEnabled(
            sorting_enabled
        )

    # =========================================================
    # SELECTION
    # =========================================================

    def selected_purchase_order(
        self,
    ) -> PurchaseOrder | None:

        row = self.currentRow()

        if row < 0:
            return None

        if row >= len(
            self._orders
        ):
            return None

        return self._orders[row]

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self._orders.clear()

        self.setRowCount(
            0
        )

    # =========================================================
    # EVENTS
    # =========================================================

    def _emit_selection(self) -> None:

        row = self.currentRow()

        if row < 0:
            return

        if row >= len(
            self._orders
        ):
            return

        self.purchase_order_selected.emit(
            self._orders[row]
        )