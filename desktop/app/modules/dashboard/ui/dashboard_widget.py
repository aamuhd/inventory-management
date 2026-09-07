from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.reports.services.report_service import (
    ReportService,
)


class DashboardCard(QFrame):

    def __init__(
        self,
        title: str,
    ) -> None:

        super().__init__()

        self.setObjectName(
            "dashboardCard"
        )

        self.setMinimumHeight(105)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        layout.setSpacing(6)

        self.title = QLabel(title)

        self.title.setObjectName(
            "dashboardCardTitle"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value = QLabel("0")

        self.value.setObjectName(
            "dashboardCardValue"
        )

        self.value.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.value
        )


class DashboardWidget(QWidget):

    def __init__(
        self,
        report_service: ReportService,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._report_service = report_service

        self._build_ui()
        self._load_dashboard()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        layout.setSpacing(8)

        # =====================================================
        # STATISTICS
        # =====================================================

        stats = QGridLayout()

        stats.setHorizontalSpacing(8)
        stats.setVerticalSpacing(8)

        self.products_card = DashboardCard(
            "Products"
        )

        self.customers_card = DashboardCard(
            "Customers"
        )

        self.suppliers_card = DashboardCard(
            "Suppliers"
        )

        self.sales_card = DashboardCard(
            "Today's Sales"
        )

        self.purchase_card = DashboardCard(
            "Today's Purchases"
        )

        self.low_stock_card = DashboardCard(
            "Low Stock"
        )

        stats.addWidget(
            self.products_card,
            0,
            0,
        )

        stats.addWidget(
            self.customers_card,
            0,
            1,
        )

        stats.addWidget(
            self.suppliers_card,
            0,
            2,
        )

        stats.addWidget(
            self.sales_card,
            1,
            0,
        )

        stats.addWidget(
            self.purchase_card,
            1,
            1,
        )

        stats.addWidget(
            self.low_stock_card,
            1,
            2,
        )

        # All three columns share the available width.
        for column in range(3):
            stats.setColumnStretch(
                column,
                1,
            )

        layout.addLayout(stats)

        # =====================================================
        # RECENT SALES
        # =====================================================

        recent_sales_label = QLabel(
            "Recent Sales"
        )

        recent_sales_label.setObjectName(
            "dashboardSectionTitle"
        )

        font = recent_sales_label.font()
        font.setBold(True)

        recent_sales_label.setFont(font)

        layout.addWidget(
            recent_sales_label
        )

        self.sales_table = QTableWidget()

        self.sales_table.setColumnCount(4)

        self.sales_table.setHorizontalHeaderLabels(
            [
                "Invoice",
                "Customer",
                "Amount",
                "Date",
            ]
        )

        self._configure_table(
            self.sales_table
        )

        # Prevent this table from consuming the entire
        # dashboard when there are many sales.
        self.sales_table.setMinimumHeight(150)
        self.sales_table.setMaximumHeight(260)

        layout.addWidget(
            self.sales_table
        )

        # =====================================================
        # LOW STOCK
        # =====================================================

        low_stock_label = QLabel(
            "Low Stock"
        )

        low_stock_label.setObjectName(
            "dashboardSectionTitle"
        )

        font = low_stock_label.font()
        font.setBold(True)

        low_stock_label.setFont(font)

        layout.addWidget(
            low_stock_label
        )

        self.low_stock_table = QTableWidget()

        self.low_stock_table.setColumnCount(2)

        self.low_stock_table.setHorizontalHeaderLabels(
            [
                "Product",
                "Stock",
            ]
        )

        self._configure_table(
            self.low_stock_table
        )

        self.low_stock_table.setMinimumHeight(
            100
        )

        self.low_stock_table.setMaximumHeight(
            220
        )

        layout.addWidget(
            self.low_stock_table
        )

        # Give the tables some room when the dashboard
        # becomes larger.
        layout.addStretch()

    # =========================================================
    # TABLE CONFIGURATION
    # =========================================================

    @staticmethod
    def _configure_table(
        table: QTableWidget,
    ) -> None:

        table.setObjectName(
            "dashboardTable"
        )

        table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        table.setAlternatingRowColors(True)

        table.setWordWrap(False)

        table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        header = table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        table.verticalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )

        table.verticalHeader().setVisible(False)
    # =========================================================
    # LOAD DASHBOARD
    # =========================================================

    def _load_dashboard(self) -> None:

        summary = (
            self._report_service.get_dashboard_summary()
        )

        # -----------------------------------------------------
        # Cards
        # -----------------------------------------------------

        self.products_card.value.setText(
            str(summary.products)
        )

        self.customers_card.value.setText(
            str(summary.customers)
        )

        self.suppliers_card.value.setText(
            str(summary.suppliers)
        )

        self.sales_card.value.setText(
            self._format_money(
                summary.today_sales
            )
        )

        self.purchase_card.value.setText(
            self._format_money(
                summary.today_purchases
            )
        )

        self.low_stock_card.value.setText(
            str(summary.low_stock)
        )

        # -----------------------------------------------------
        # Tables
        # -----------------------------------------------------

        self._load_recent_sales(
            summary.recent_sales
        )

        self._load_low_stock(
            summary.low_stock_products
        )

    # =========================================================
    # RECENT SALES
    # =========================================================

    def _load_recent_sales(
        self,
        sales,
    ) -> None:

        self.sales_table.setRowCount(
            len(sales)
        )

        for row, sale in enumerate(sales):

            values = [
                str(sale.invoice),
                str(sale.customer),
                self._format_money(
                    sale.amount
                ),
                str(sale.date),
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(
                    value
                )

                if column == 2:

                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight
                        | Qt.AlignmentFlag.AlignVCenter
                    )

                self.sales_table.setItem(
                    row,
                    column,
                    item,
                )

        self.sales_table.resizeRowsToContents()

    # =========================================================
    # LOW STOCK
    # =========================================================

    def _load_low_stock(
        self,
        products,
    ) -> None:

        self.low_stock_table.setRowCount(
            len(products)
        )

        for row, product in enumerate(products):

            values = [
                str(product.product),
                str(product.stock),
            ]

            for column, value in enumerate(values):

                item = QTableWidgetItem(
                    value
                )

                if column == 1:

                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight
                        | Qt.AlignmentFlag.AlignVCenter
                    )

                self.low_stock_table.setItem(
                    row,
                    column,
                    item,
                )

        self.low_stock_table.resizeRowsToContents()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self) -> None:

        self._load_dashboard()

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _format_money(
        value: Decimal,
    ) -> str:

        return f"₦{value:,.2f}"