from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.models.supplier import Supplier


class SupplierTable(QWidget):
    """
    Displays suppliers in a table.

    This widget is responsible only for displaying data.
    It does not communicate with the service layer.
    """

    supplier_selected = Signal(Supplier)

    def __init__(self) -> None:
        super().__init__()

        self._suppliers: list[Supplier] = []

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
                "Name",
                "Contact Person",
                "Phone",
                "Email",
                "Address",
                "Notes",
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

    def set_suppliers(
        self,
        suppliers: list[Supplier],
    ) -> None:
        """
        Populate the table with suppliers.
        """

        self._suppliers = suppliers

        self.table.setRowCount(len(suppliers))

        for row, supplier in enumerate(suppliers):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(supplier.name),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    supplier.contact_person or ""
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    supplier.phone or ""
                ),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    supplier.email or ""
                ),
            )

            self.table.setItem(
                row,
                4,
                QTableWidgetItem(
                    supplier.address or ""
                ),
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(
                    supplier.notes or ""
                ),
            )

    def selected_supplier(
        self,
    ) -> Supplier | None:
        """
        Returns the currently selected supplier.
        """

        row = self.table.currentRow()

        if row < 0:
            return None

        if row >= len(self._suppliers):
            return None

        return self._suppliers[row]

    def clear(self) -> None:
        """
        Clears the table.
        """

        self._suppliers.clear()

        self.table.setRowCount(0)

    def _on_item_double_clicked(
        self,
    ) -> None:

        supplier = self.selected_supplier()

        if supplier is not None:

            self.supplier_selected.emit(
                supplier,
            )