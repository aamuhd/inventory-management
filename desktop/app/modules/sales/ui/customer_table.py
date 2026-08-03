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
    Displays Customers in a table.

    This widget is responsible only for displaying data.
    It does not communicate with the service layer.
    """

    customer_selected = Signal(Customer)

    def __init__(self) -> None:
        super().__init__()

        self._customers: list[Customer] = []

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

        self.table.setAlternatingRowColors(True)

        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout = QVBoxLayout(self)

        layout.addWidget(self.table)

    def set_customers(
        self,
        customers: list[Customer],
    ) -> None:
        """
        Populate the table with Customers.
        """

        self._customers = customers

        self.table.setRowCount(len(customers))

        for row, customer in enumerate(customers):

            self.table.setItem(
                row,
                0,
                QTableWidgetItem(customer.name),
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


    def selected_customer(
        self,
    ) -> Customer | None:
        """
        Returns the currently selected Customer.
        """

        row = self.table.currentRow()

        if row < 0:
            return None

        if row >= len(self._customers):
            return None

        return self._customers[row]

    def clear(self) -> None:
        """
        Clears the table.
        """

        self._customers.clear()

        self.table.setRowCount(0)

    def _on_item_double_clicked(
        self,
    ) -> None:

        customer = self.selected_customer()

        if customer is not None:

            self.customer_selected.emit(
                customer,
            )