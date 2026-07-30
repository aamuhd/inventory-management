from __future__ import annotations
from typing import TYPE_CHECKING

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

if TYPE_CHECKING:
    from app.modules.inventory.models.product_variant import ProductVariant


class ProductVariantTable(QWidget):

    variant_selected = Signal(object)

    def __init__(self) -> None:
        super().__init__()

        self._variants: list[ProductVariant] = []

        self.table = QTableWidget()

        self.table.setColumnCount(8)

        self.table.setHorizontalHeaderLabels(
            [
                "Product",
                "Length",
                "Stock",
                "Reorder",
                "Cost Price",
                "Selling Price",
                "SKU",
                "Barcode",
            ]
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows,
        )

        self.table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection,
        )

        self.table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers,
        )

        self.table.cellClicked.connect(
            self._row_selected,
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    def set_variants(
        self,
        variants: list[ProductVariant],
    ) -> None:

        self._variants = variants

        self.table.setRowCount(len(variants))

        for row, variant in enumerate(variants):

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
                    str(
                        variant.length,
                    ),
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    str(
                        variant.stock_quantity,
                    ),
                ),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    str(
                        variant.reorder_level,
                    ),
                ),
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    str(
                        variant.cost_price,
                    ),
                ),
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(
                    str(
                        variant.selling_price,
                    ),
                ),
            )

            self.table.setItem(
                row,
                6,
                QTableWidgetItem(
                    variant.sku or "",
                ),
            )

            self.table.setItem(
                row,
                7,
                QTableWidgetItem(
                    variant.barcode or "",
                ),
            )

        self.table.resizeColumnsToContents()

    def _row_selected(
        self,
        row: int,
        column: int,
    ) -> None:

        del column

        if row >= len(self._variants):
            return

        self.variant_selected.emit(
            self._variants[row],
        )

    def selected_variant(
        self,
    ) -> ProductVariant | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        return self._variants[row]

    def clear_selection(
        self,
    ) -> None:

        self.table.clearSelection()