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

from app.modules.inventory.models.category import Category


class CategoryTable(QWidget):
    """
    Displays categories in a responsive table.

    This widget is responsible only for displaying data.
    It does not communicate with the service layer.
    """

    category_selected = Signal(Category)

    def __init__(self) -> None:

        super().__init__()

        self._categories: list[Category] = []

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setObjectName(
            "categoryTableContainer"
        )

        self.table = QTableWidget()

        self.table.setObjectName(
            "categoryTable"
        )

        self.table.setColumnCount(
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
                "Description",
                "Created",
            ]
        )

        # -----------------------------------------------------
        # Selection
        # -----------------------------------------------------

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        # -----------------------------------------------------
        # Appearance
        # -----------------------------------------------------

        self.table.setAlternatingRowColors(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setWordWrap(
            False
        )

        # -----------------------------------------------------
        # Sorting
        # -----------------------------------------------------

        self.table.setSortingEnabled(
            True
        )

        # -----------------------------------------------------
        # Responsive columns
        # -----------------------------------------------------

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        header.setMinimumSectionSize(
            80
        )

        # -----------------------------------------------------
        # Double-click
        # -----------------------------------------------------

        self.table.itemDoubleClicked.connect(
            self._on_item_double_clicked
        )

        # -----------------------------------------------------
        # Layout
        # -----------------------------------------------------

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

    def set_categories(
        self,
        categories: list[Category],
    ) -> None:

        self._categories = categories

        # Temporarily disable sorting while
        # populating the table.
        sorting_enabled = (
            self.table.isSortingEnabled()
        )

        self.table.setSortingEnabled(
            False
        )

        self.table.setRowCount(
            len(categories)
        )

        for row, category in enumerate(
            categories
        ):

            # -------------------------------------------------
            # ID
            # -------------------------------------------------

            id_item = QTableWidgetItem(
                str(category.id)
            )

            # Store the actual Category ID
            # inside the table item.
            id_item.setData(
                Qt.ItemDataRole.UserRole,
                category.id,
            )

            self.table.setItem(
                row,
                0,
                id_item,
            )

            # -------------------------------------------------
            # Name
            # -------------------------------------------------

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    category.name
                ),
            )

            # -------------------------------------------------
            # Description
            # -------------------------------------------------

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    category.description
                ),
            )

            # -------------------------------------------------
            # Created
            # -------------------------------------------------

            created = (
                category.created_at.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    created
                ),
            )

        self.table.setSortingEnabled(
            sorting_enabled
        )

    # =========================================================
    # SELECTION
    # =========================================================

    def selected_category(
        self,
    ) -> Category | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        id_item = self.table.item(
            row,
            0,
        )

        if id_item is None:
            return None

        category_id = id_item.data(
            Qt.ItemDataRole.UserRole
        )

        for category in self._categories:

            if category.id == category_id:
                return category

        return None

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(
        self,
    ) -> None:

        self._categories.clear()

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

        category = (
            self.selected_category()
        )

        if category is not None:

            self.category_selected.emit(
                category
            )