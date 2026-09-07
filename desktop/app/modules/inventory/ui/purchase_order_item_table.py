from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
)

from app.modules.inventory.models.purchase_order_item import (
    PurchaseOrderItem,
)


class PurchaseOrderItemTable(QTableWidget):

    item_selected = Signal(PurchaseOrderItem)

    def __init__(self) -> None:
        super().__init__()

        self._items: list[PurchaseOrderItem] = []

        self.setObjectName(
            "purchaseOrderItemTable"
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

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

        self.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection,
        )

        self.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers,
        )

        self.setAlternatingRowColors(True)

        self.verticalHeader().setVisible(False)

        self.setSortingEnabled(True)

        self.setWordWrap(False)

        self.setTextElideMode(
            Qt.TextElideMode.ElideRight
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = self.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeMode.Stretch,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.ResizeMode.ResizeToContents,
        )

        header.setMinimumSectionSize(90)

        # -----------------------------------------------------
        # Signals
        # -----------------------------------------------------

        self.itemSelectionChanged.connect(
            self._emit_selection,
        )

    # =========================================================
    # LOAD
    # =========================================================

    def load(
        self,
        items: list[PurchaseOrderItem],
    ) -> None:

        self._items = items

        sorting_enabled = (
            self.isSortingEnabled()
        )

        self.setSortingEnabled(False)

        self.setRowCount(
            len(items)
        )

        for row, item in enumerate(items):

            variant = ""

            if item.product_variant:

                if item.product_variant.sku:

                    variant = (
                        item.product_variant.sku
                    )

                else:

                    variant = str(
                        item.product_variant.length
                    )

            subtotal = (
                item.quantity
                * item.unit_cost
            )

            # -------------------------------------------------
            # Variant
            # -------------------------------------------------

            variant_item = QTableWidgetItem(
                variant
            )

            self.setItem(
                row,
                0,
                variant_item,
            )

            # -------------------------------------------------
            # Quantity
            # -------------------------------------------------

            quantity_item = QTableWidgetItem(
                str(item.quantity)
            )

            quantity_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

            self.setItem(
                row,
                1,
                quantity_item,
            )

            # -------------------------------------------------
            # Cost Price
            # -------------------------------------------------

            cost_item = QTableWidgetItem(
                str(item.unit_cost)
            )

            cost_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

            self.setItem(
                row,
                2,
                cost_item,
            )

            # -------------------------------------------------
            # Subtotal
            # -------------------------------------------------

            subtotal_item = QTableWidgetItem(
                str(subtotal)
            )

            subtotal_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

            self.setItem(
                row,
                3,
                subtotal_item,
            )

        self.setSortingEnabled(
            sorting_enabled
        )

    # =========================================================
    # SELECTED ITEM
    # =========================================================

    def selected_item(
        self,
    ) -> PurchaseOrderItem | None:

        row = self.currentRow()

        if row < 0:
            return None

        if row >= len(self._items):
            return None

        return self._items[row]

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self._items.clear()

        self.setRowCount(0)

    # =========================================================
    # SIGNAL
    # =========================================================

    def _emit_selection(self) -> None:

        row = self.currentRow()

        if row < 0:
            return

        if row >= len(self._items):
            return

        self.item_selected.emit(
            self._items[row]
        )