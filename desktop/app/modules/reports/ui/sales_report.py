from datetime import date
from decimal import Decimal

from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QVBoxLayout,
    QWidget,
)


class SalesReport(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()

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
            12
        )

        # -----------------------------------------------------
        # Sales Summary
        # -----------------------------------------------------

        summary_group = QGroupBox(
            "Sales Summary"
        )

        summary_layout = QGridLayout(
            summary_group
        )

        self._total_sales_label = QLabel(
            "₦0.00"
        )

        self._number_of_sales_label = QLabel(
            "0"
        )

        self._items_sold_label = QLabel(
            "0"
        )

        self._average_sale_label = QLabel(
            "₦0.00"
        )

        summary_layout.addWidget(
            QLabel("Total Sales"),
            0,
            0,
        )

        summary_layout.addWidget(
            self._total_sales_label,
            0,
            1,
        )

        summary_layout.addWidget(
            QLabel("Number of Sales"),
            1,
            0,
        )

        summary_layout.addWidget(
            self._number_of_sales_label,
            1,
            1,
        )

        summary_layout.addWidget(
            QLabel("Items Sold"),
            2,
            0,
        )

        summary_layout.addWidget(
            self._items_sold_label,
            2,
            1,
        )

        summary_layout.addWidget(
            QLabel("Average Sale"),
            3,
            0,
        )

        summary_layout.addWidget(
            self._average_sale_label,
            3,
            1,
        )

        main_layout.addWidget(
            summary_group
        )

        # -----------------------------------------------------
        # Sales Details
        # -----------------------------------------------------

        details_group = QGroupBox(
            "Sales Details"
        )

        details_layout = QVBoxLayout(
            details_group
        )

        self._details_label = QLabel(
            "Detailed sales information will appear here."
        )

        self._details_label.setWordWrap(
            True
        )

        details_layout.addWidget(
            self._details_label
        )

        main_layout.addWidget(
            details_group,
            1,
        )

    # =========================================================
    # DATA
    # =========================================================

    def set_data(
        self,
        sales,
    ) -> None:

        self._total_sales_label.setText(
            self._format_money(
                sales.total_sales
            )
        )

        self._number_of_sales_label.setText(
            str(
                sales.number_of_sales
            )
        )

        self._items_sold_label.setText(
            str(
                sales.total_items_sold
            )
        )

        self._average_sale_label.setText(
            self._format_money(
                sales.average_sale
            )
        )

    # =========================================================
    # REPORT LOADING
    # =========================================================

    def load_report(
        self,
        report_service,
        *,
        start_date: date,
        end_date: date,
    ) -> None:

        sales = (
            report_service.get_sales_summary(
                start_date=start_date,
                end_date=end_date,
            )
        )

        self.set_data(
            sales
        )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _format_money(
        value: Decimal,
    ) -> str:

        return f"₦{value:,.2f}"