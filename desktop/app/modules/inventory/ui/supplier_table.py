from PySide6.QtCore import Qt, Signal
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
    Displays suppliers in a responsive table.

    This widget is responsible only for displaying data.
    It does not communicate with the service layer.
    """

    supplier_selected = Signal(Supplier)

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName(
            "supplierTableContainer"
        )

        self._suppliers: list[Supplier] = []

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.table = QTableWidget()

        self.table.setObjectName(
            "supplierTable"
        )

        self.table.itemDoubleClicked.connect(
            self._on_item_double_clicked
        )

        self.table.setSortingEnabled(
            True
        )

        self.table.setColumnCount(
            6
        )

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

        self.table.setTextElideMode(
            Qt.TextElideMode.ElideRight
        )

        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        self.table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        # -----------------------------------------------------
        # Columns
        # -----------------------------------------------------

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )

        header.resizeSection(
            0,
            160,
        )

        header.resizeSection(
            1,
            150,
        )

        header.resizeSection(
            2,
            130,
        )

        header.resizeSection(
            3,
            180,
        )

        header.resizeSection(
            4,
            220,
        )

        header.resizeSection(
            5,
            220,
        )

        header.setMinimumSectionSize(
            80
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

    def set_suppliers(
        self,
        suppliers: list[Supplier],
    ) -> None:

        self._suppliers = suppliers

        sorting_enabled = (
            self.table.isSortingEnabled()
        )

        self.table.setSortingEnabled(
            False
        )

        self.table.setRowCount(
            len(suppliers)
        )

        for row, supplier in enumerate(
            suppliers
        ):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    supplier.name
                ),
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

        self.table.setSortingEnabled(
            sorting_enabled
        )

    # =========================================================
    # SELECTION
    # =========================================================

    def selected_supplier(
        self,
    ) -> Supplier | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        if row >= len(
            self._suppliers
        ):
            return None

        return self._suppliers[row]

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(
        self,
    ) -> None:

        self._suppliers.clear()

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

        supplier = (
            self.selected_supplier()
        )

        if supplier is not None:

            self.supplier_selected.emit(
                supplier
            )