from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.sales.models.customer import Customer


class CustomerTable(QWidget):
    """
    Displays customers in a table.

    This widget is responsible only for displaying data.
    It does not communicate with the service layer.
    """

    customer_selected = Signal(Customer)

    def __init__(self) -> None:
        super().__init__()

        self.setObjectName(
            "customerTable"
        )

        self._customers: list[Customer] = []

        self._build_ui()

    def _build_ui(self) -> None:

        # =====================================================
        # TABLE
        # =====================================================

        self.table = QTableWidget()

        self.table.setObjectName(
            "customerTableWidget"
        )

        self.table.setColumnCount(
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Name",
                "Phone",
                "Email",
                "Address",
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

        self.table.setSortingEnabled(
            True
        )

        self.table.verticalHeader().setVisible(
            False
        )

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # -----------------------------------------------------
        # Double click
        # -----------------------------------------------------

        self.table.itemDoubleClicked.connect(
            self._on_item_double_clicked
        )

        # =====================================================
        # LAYOUT
        # =====================================================

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
    # LOAD
    # =========================================================

    def set_customers(
        self,
        customers: list[Customer],
    ) -> None:
        """
        Populate the table with customers.
        """

        self._customers = list(
            customers
        )

        self.table.setRowCount(
            len(self._customers)
        )

        for row, customer in enumerate(
            self._customers
        ):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(
                    customer.name
                ),
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    customer.phone or ""
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    customer.email or ""
                ),
            )

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    customer.address or ""
                ),
            )

    # =========================================================
    # SELECTION
    # =========================================================

    def selected_customer(
        self,
    ) -> Customer | None:
        """
        Return the currently selected customer.
        """

        row = self.table.currentRow()

        if row < 0:
            return None

        if row >= len(
            self._customers
        ):
            return None

        return self._customers[row]

    def _on_item_double_clicked(
        self,
        _item,
    ) -> None:

        customer = (
            self.selected_customer()
        )

        if customer is not None:

            self.customer_selected.emit(
                customer
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:
        """
        Clear the table.
        """

        self.table.clearContents()

        self.table.setRowCount(
            0
        )

        self._customers.clear()