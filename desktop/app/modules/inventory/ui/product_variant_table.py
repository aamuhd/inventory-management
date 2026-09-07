from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractScrollArea,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.models.product_variant import ProductVariant


class ProductVariantTable(QWidget):

    variant_selected = Signal(ProductVariant)

    def __init__(self) -> None:
        super().__init__()

        self._variants: list[ProductVariant] = []

        self.setObjectName(
            "productVariantTableContainer"
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.table = QTableWidget()

        self.table.setObjectName(
            "productVariantTable"
        )

        self.table.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored
        )

        self.table.setSortingEnabled(
            True
        )

        self.table.setColumnCount(
            9
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Product",
                "Variant",
                "Length",
                "SKU",
                "Stock",
                "Reorder Level",
                "Cost Price",
                "Selling Price",
                "Created",
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

        self.table.setWordWrap(
            False
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        header.setMinimumSectionSize(
            80
        )

        header.setStretchLastSection(
            True
        )

        self.table.itemDoubleClicked.connect(
            self._on_item_double_clicked
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            self.table
        )

    # =========================================================
    # DATA
    # =========================================================

    def set_variants(
        self,
        variants: list[ProductVariant],
        product_names: dict,
    ) -> None:

        self._variants = list(
            variants
        )

        sorting_enabled = (
            self.table.isSortingEnabled()
        )

        self.table.setSortingEnabled(
            False
        )

        self.table.setRowCount(
            len(variants)
        )

        for row, variant in enumerate(
            variants
        ):

            # -------------------------------------------------
            # Product
            # -------------------------------------------------

            product_name = product_names.get(
                variant.product_id,
                "",
            )

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    product_name
                ),
            )

            # -------------------------------------------------
            # Variant
            # -------------------------------------------------

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    variant.name
                ),
            )

            # -------------------------------------------------
            # Length
            # -------------------------------------------------

            length_item = QTableWidgetItem(
                str(variant.length)
            )

            length_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

            self.table.setItem(
                row,
                2,
                length_item,
            )

            # -------------------------------------------------
            # SKU
            # -------------------------------------------------

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    variant.sku or ""
                ),
            )

            # -------------------------------------------------
            # Stock
            # -------------------------------------------------

            stock_item = QTableWidgetItem(
                str(variant.stock_quantity)
            )

            stock_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

            self.table.setItem(
                row,
                4,
                stock_item,
            )

            # -------------------------------------------------
            # Reorder Level
            # -------------------------------------------------

            reorder_item = QTableWidgetItem(
                str(variant.reorder_level)
            )

            reorder_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

            self.table.setItem(
                row,
                5,
                reorder_item,
            )

            # -------------------------------------------------
            # Cost Price
            # -------------------------------------------------

            cost_item = QTableWidgetItem(
                str(variant.cost_price)
            )

            cost_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

            self.table.setItem(
                row,
                6,
                cost_item,
            )

            # -------------------------------------------------
            # Selling Price
            # -------------------------------------------------

            selling_item = QTableWidgetItem(
                str(variant.selling_price)
            )

            selling_item.setTextAlignment(
                Qt.AlignmentFlag.AlignRight
                | Qt.AlignmentFlag.AlignVCenter
            )

            self.table.setItem(
                row,
                7,
                selling_item,
            )

            # -------------------------------------------------
            # Created
            # -------------------------------------------------

            created = (
                variant.created_at.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

            self.table.setItem(
                row,
                8,
                QTableWidgetItem(
                    created
                ),
            )

            # -------------------------------------------------
            # Store UUID on the first column
            # -------------------------------------------------

            product_item = self.table.item(
                row,
                0,
            )

            if product_item is not None:

                product_item.setData(
                    Qt.ItemDataRole.UserRole,
                    variant.id,
                )

        self.table.setSortingEnabled(
            sorting_enabled
        )

    # =========================================================
    # SELECTION
    # =========================================================

    def selected_variant(
        self,
    ) -> ProductVariant | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(
            row,
            0,
        )

        if item is None:
            return None

        variant_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if variant_id is None:
            return None

        for variant in self._variants:

            if variant.id == variant_id:
                return variant

        return None

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self._variants.clear()

        self.table.setRowCount(
            0
        )

    # =========================================================
    # EVENTS
    # =========================================================

    def _on_item_double_clicked(
        self,
        item: QTableWidgetItem,
    ) -> None:

        variant = self.selected_variant()

        if variant is not None:

            self.variant_selected.emit(
                variant
            )