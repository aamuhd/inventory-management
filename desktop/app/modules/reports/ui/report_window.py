from datetime import date

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QDateEdit,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
)

from app.core.ui.base_window import BaseWindow

from app.modules.reports.services.report_service import (
    ReportService,
)

from app.modules.reports.ui.overview_report import (
    OverviewReport,
)

from app.modules.reports.ui.sales_report import (
    SalesReport,
)

from app.modules.reports.ui.inventory_report import (
    InventoryReport,
)

from app.modules.reports.ui.purchase_report import (
    PurchasesReport,
)

from app.modules.reports.ui.returns_report import (
    ReturnsReport,
)

from app.modules.reports.ui.stock_movement_report import (
    StockMovementReport,
)


class ReportsWindow(BaseWindow):

    def __init__(
        self,
        report_service: ReportService,
    ) -> None:

        super().__init__()

        self._report_service = report_service

        self.setWindowTitle(
            "Reports"
        )

        self.resize(
            1100,
            750,
        )

        self._build_ui()

        self._load_report()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        main_layout.setSpacing(
            10,
        )

        # -----------------------------------------------------
        # Date Filter
        # -----------------------------------------------------

        filter_layout = QHBoxLayout()

        filter_layout.addWidget(
            QLabel("From:")
        )

        self._start_date = QDateEdit()

        self._start_date.setCalendarPopup(
            True,
        )

        self._start_date.setDate(
            QDate.currentDate(),
        )

        filter_layout.addWidget(
            self._start_date,
        )

        filter_layout.addWidget(
            QLabel("To:")
        )

        self._end_date = QDateEdit()

        self._end_date.setCalendarPopup(
            True,
        )

        self._end_date.setDate(
            QDate.currentDate(),
        )

        filter_layout.addWidget(
            self._end_date,
        )

        self._generate_button = QPushButton(
            "Generate Report",
        )

        self._generate_button.clicked.connect(
            self._load_report,
        )

        filter_layout.addWidget(
            self._generate_button,
        )

        filter_layout.addStretch()

        main_layout.addLayout(
            filter_layout,
        )

        # -----------------------------------------------------
        # Report Tabs
        # -----------------------------------------------------

        self._tabs = QTabWidget()

        self._overview_report = (
            OverviewReport()
        )

        self._sales_report = (
            SalesReport()
        )

        self._inventory_report = (
            InventoryReport(
                self._report_service,
            )
        )

        self._purchase_report = (
            PurchasesReport(
                self._report_service,
            )
        )

        self._returns_report = (
            ReturnsReport(
                self._report_service,
            )
        )

        self._stock_movement_report = (
            StockMovementReport(
                self._report_service,
            )
        )

        self._tabs.addTab(
            self._overview_report,
            "Overview",
        )

        self._tabs.addTab(
            self._sales_report,
            "Sales",
        )

        self._tabs.addTab(
            self._inventory_report,
            "Inventory",
        )

        self._tabs.addTab(
            self._purchase_report,
            "Purchases",
        )

        self._tabs.addTab(
            self._returns_report,
            "Returns",
        )

        self._tabs.addTab(
            self._stock_movement_report,
            "Stock Movements",
        )

        main_layout.addWidget(
            self._tabs,
            1,
        )

    # =========================================================
    # REPORT LOADING
    # =========================================================

    def _load_report(self) -> None:

        start_date = (
            self._qdate_to_date(
                self._start_date.date(),
            )
        )

        end_date = (
            self._qdate_to_date(
                self._end_date.date(),
            )
        )

        if start_date > end_date:

            QMessageBox.warning(
                self,
                "Invalid Date Range",
                (
                    "The start date cannot be "
                    "later than the end date."
                ),
            )

            return

        try:

            # =================================================
            # Fetch all report data ONCE
            # =================================================

            sales = (
                self._report_service
                .get_sales_summary(
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            inventory = (
                self._report_service
                .get_inventory_summary()
            )

            purchases = (
                self._report_service
                .get_purchase_summary(
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            returns = (
                self._report_service
                .get_sales_return_summary(
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            movements = (
                self._report_service
                .get_stock_movement_summary(
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            movement_history = (
                self._report_service
                .get_stock_movement_history(
                    start_date=start_date,
                    end_date=end_date,
                )
            )

            # =================================================
            # Update Overview
            # =================================================

            self._overview_report.set_data(
                sales=sales,
                inventory=inventory,
                purchases=purchases,
                returns=returns,
                movements=movements,
            )

            # =================================================
            # Update Sales
            # =================================================

            self._sales_report.set_data(
                sales,
            )

            # =================================================
            # Update Inventory
            # =================================================

            self._inventory_report.set_data(
                inventory,
            )

            # =================================================
            # Update Purchases
            # =================================================

            self._purchase_report.set_data(
                purchases,
            )

            # =================================================
            # Update Returns
            # =================================================

            self._returns_report.set_data(
                returns,
                number_of_sales=(
                    sales.number_of_sales
                ),
                total_items_sold=(
                    sales.total_items_sold
                ),
            )

            # =================================================
            # Update Stock Movements
            # =================================================

            self._stock_movement_report.set_data(
                movements=movements,
                history=movement_history,
            )

        except Exception as error:

            self.show_error(
                str(error),
            )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _qdate_to_date(
        value: QDate,
    ) -> date:

        return date(
            value.year(),
            value.month(),
            value.day(),
        )