from __future__ import annotations

from uuid import UUID

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.models.product import Product


class ProductTable(QWidget):
    """
    Displays products in a table.

    This widget is responsible only for displaying data.
    It does not communicate with the service layer.
    """

    product_selected = Signal(Product)

    def __init__(self) -> None:
        super().__init__()

        self._products: list[Product] = []

        self._build_ui()

    def _build_ui(self) -> None:
        self.table = QTableWidget()

        self.table.itemDoubleClicked.connect(
            self._on_item_double_clicked
        )

        self.table.setSortingEnabled(True)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Brand",
                "Category",
                "Description",
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

        self.table.setAlternatingRowColors(True)

        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    def set_products(
        self,
        products: list[Product],
        category_names: dict[int, str],
    ) -> None:
        """
        Populate the table with products.
        """

        self._products = products

        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(str(product.id)),
            )
            self.table.setItem(
                row,
                1,
                QTableWidgetItem(product.name),
            )
            self.table.setItem(
                row,
                2,
                QTableWidgetItem(product.brand or ""),
            )

            if product.category_id is None:
                category_name = ""
            else:
                category_name = category_names.get(
                    product.category_id,
                    "",
                )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(category_name),
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(product.description or ""),
            )

            created = product.created_at.strftime(
                "%Y-%m-%d %H:%M"
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(created),
            )

    def selected_product(self) -> Product | None:
        """
        Returns the currently selected product.
        """

        row = self.table.currentRow()

        if row < 0:
            return None

        if row >= len(self._products):
            return None

        return self._products[row]

    def clear(self) -> None:
        """
        Clears the table.
        """

        self._products.clear()

        self.table.setRowCount(0)

    def _on_item_double_clicked(self) -> None:
        product = self.selected_product()

        if product is not None:
            self.product_selected.emit(product)