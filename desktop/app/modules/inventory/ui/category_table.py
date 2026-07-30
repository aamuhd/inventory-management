from __future__ import annotations

from PySide6.QtCore import Signal, Slot
from PySide6.QtCore import Qt
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
    Displays categories in a table.

    This widget is responsible only for displaying data.
    It does not communicate with the service layer.
    """
    category_selected = Signal(Category)

    def __init__(self) -> None:
        super().__init__()

        self._categories: list[Category] = []

        self._build_ui()

    def _build_ui(self) -> None:
        self.table = QTableWidget()

        self.table.itemDoubleClicked.connect(
            self._on_item_double_clicked
        )

        self.table.setSortingEnabled(True)

        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Name",
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
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        layout = QVBoxLayout(self)
        layout.addWidget(self.table)

    def set_categories(
        self,
        categories: list[Category],
    ) -> None:
        """
        Populate the table with categories.
        """

        self._categories = categories

        self.table.setRowCount(len(categories))

        for row, category in enumerate(categories):
            self.table.setItem(
                row,
                0,
                QTableWidgetItem(str(category.id)),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(category.name),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(category.description),
            )

            created = category.created_at.strftime(
                "%Y-%m-%d %H:%M"
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(created),
            )

    def selected_category(self) -> Category | None:
        """
        Returns the currently selected Category.
        """

        row = self.table.currentRow()

        if row < 0:
            return None

        if row >= len(self._categories):
            return None

        return self._categories[row]

    def clear(self) -> None:
        """
        Clears the table.
        """

        self._categories.clear()

        self.table.setRowCount(0)
    
    def _on_item_double_clicked(self):
        category = self.selected_category()

        if category is not None:
            self.category_selected.emit(category)