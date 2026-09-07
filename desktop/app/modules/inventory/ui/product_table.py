from __future__ import annotations

from PySide6.QtCore import Qt, Signal
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

    product_selected = Signal(Product)

    def __init__(self) -> None:
        super().__init__()

        self._products: list[Product] = []

        self.setObjectName(
            "productTableContainer"
        )

        self._build_ui()

    def _build_ui(self) -> None:

        self.table = QTableWidget()

        self.table.setObjectName(
            "productTable"
        )

        self.table.setSortingEnabled(
            True
        )

        self.table.setColumnCount(
            6
        )

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

        self.table.setAlternatingRowColors(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setWordWrap(
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
            QHeaderView.ResizeMode.Interactive
        )

        header.resizeSection(0, 180)
        header.resizeSection(1, 160)
        header.resizeSection(2, 140)
        header.resizeSection(3, 160)
        header.resizeSection(4, 220)
        header.resizeSection(5, 150)

        # -----------------------------------------------------
        # Hide ID column from the user.
        #
        # The ID is still stored in column 0 internally so
        # selected_product() can continue to identify the
        # selected Product correctly.
        # -----------------------------------------------------

        self.table.setColumnHidden(
            0,
            True,
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

    def set_products(
        self,
        products: list[Product],
        category_names: dict[int, str],
    ) -> None:

        self._products = products

        sorting_enabled = (
            self.table.isSortingEnabled()
        )

        self.table.setSortingEnabled(
            False
        )

        self.table.setRowCount(
            len(products)
        )

        for row, product in enumerate(
            products
        ):

            id_item = QTableWidgetItem(
                str(product.id)
            )

            id_item.setData(
                Qt.ItemDataRole.UserRole,
                product.id,
            )

            self.table.setItem(
                row,
                0,
                id_item,
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    product.name
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    product.brand or ""
                ),
            )

            category_name = ""

            if product.category_id is not None:

                category_name = (
                    category_names.get(
                        product.category_id,
                        "",
                    )
                )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    category_name
                ),
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    product.description or ""
                ),
            )

            created = (
                product.created_at.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(
                    created
                ),
            )

        self.table.setSortingEnabled(
            sorting_enabled
        )

        # Make sure the ID remains hidden even after
        # refreshing the table.
        self.table.setColumnHidden(
            0,
            True,
        )

    def selected_product(
        self,
    ) -> Product | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        id_item = self.table.item(
            row,
            0,
        )

        if id_item is None:
            return None

        product_id = id_item.data(
            Qt.ItemDataRole.UserRole
        )

        for product in self._products:

            if product.id == product_id:
                return product

        return None

    def clear(self) -> None:

        self._products.clear()

        self.table.setRowCount(
            0
        )

    def _on_item_double_clicked(
        self,
        item: QTableWidgetItem,
    ) -> None:

        product = self.selected_product()

        if product is not None:

            self.product_selected.emit(
                product
            )
