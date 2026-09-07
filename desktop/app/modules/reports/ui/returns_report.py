from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class ReturnsReport(QWidget):

    def __init__(
        self,
        report_service,
        parent: QWidget | None = None,
    ) -> None:

        super().__init__(parent)

        self._report_service = report_service

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        outer_layout = QVBoxLayout(self)

        outer_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        # -----------------------------------------------------
        # Scroll Area
        # -----------------------------------------------------

        scroll_area = QScrollArea()

        scroll_area.setWidgetResizable(True)

        scroll_area.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        content = QWidget()

        main_layout = QVBoxLayout(content)

        main_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        main_layout.setSpacing(16)

        # -----------------------------------------------------
        # Returns Overview
        # -----------------------------------------------------

        overview_group = QGroupBox(
            "Returns Overview"
        )

        overview_layout = QGridLayout()

        overview_layout.setContentsMargins(
            12,
            12,
            12,
            12,
        )

        overview_layout.setHorizontalSpacing(
            24
        )

        overview_layout.setVerticalSpacing(
            8
        )

        self._returns_count_label = (
            self._create_value_label("0")
        )

        self._returns_amount_label = (
            self._create_value_label("₹0.00")
        )

        self._returned_items_label = (
            self._create_value_label("0")
        )

        self._average_return_label = (
            self._create_value_label("₹0.00")
        )

        self._add_metric(
            overview_layout,
            0,
            0,
            "Number of Returns",
            self._returns_count_label,
        )

        self._add_metric(
            overview_layout,
            0,
            1,
            "Return Amount",
            self._returns_amount_label,
        )

        self._add_metric(
            overview_layout,
            1,
            0,
            "Items Returned",
            self._returned_items_label,
        )

        self._add_metric(
            overview_layout,
            1,
            1,
            "Average Return",
            self._average_return_label,
        )

        overview_group.setLayout(
            overview_layout
        )

        overview_group.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        main_layout.addWidget(
            overview_group
        )

        # -----------------------------------------------------
        # Return Analysis
        # -----------------------------------------------------

        analysis_group = QGroupBox(
            "Return Analysis"
        )

        analysis_layout = QGridLayout()

        analysis_layout.setHorizontalSpacing(
            16
        )

        analysis_layout.setVerticalSpacing(
            12
        )

        self._return_rate_label = (
            self._create_value_label("0.00%")
        )

        self._returned_items_rate_label = (
            self._create_value_label("0.00%")
        )

        analysis_layout.addWidget(
            QLabel("Return Rate"),
            0,
            0,
        )

        analysis_layout.addWidget(
            self._return_rate_label,
            0,
            1,
        )

        analysis_layout.addWidget(
            QLabel("Returned Items Rate"),
            1,
            0,
        )

        analysis_layout.addWidget(
            self._returned_items_rate_label,
            1,
            1,
        )

        analysis_group.setLayout(
            analysis_layout
        )

        main_layout.addWidget(
            analysis_group
        )

        # -----------------------------------------------------
        # Information
        # -----------------------------------------------------

        information_group = QGroupBox(
            "Return Information"
        )

        information_layout = QVBoxLayout()

        self._information_label = QLabel(
            "Return information for the selected period."
        )

        self._information_label.setWordWrap(
            True
        )

        information_layout.addWidget(
            self._information_label
        )

        information_group.setLayout(
            information_layout
        )

        main_layout.addWidget(
            information_group
        )

        main_layout.addStretch()

        scroll_area.setWidget(
            content
        )

        outer_layout.addWidget(
            scroll_area
        )

    # =========================================================
    # DATA
    # =========================================================

    def set_data(
        self,
        returns,
        *,
        number_of_sales: int = 0,
        total_items_sold: int = 0,
    ) -> None:

        number_of_returns = (
            returns.number_of_returns
        )

        total_return_amount = (
            returns.total_return_amount
        )

        total_items_returned = (
            returns.total_items_returned
        )

        # -----------------------------------------------------
        # Overview
        # -----------------------------------------------------

        self._returns_count_label.setText(
            str(number_of_returns)
        )

        self._returns_amount_label.setText(
            self._format_money(
                total_return_amount
            )
        )

        self._returned_items_label.setText(
            str(total_items_returned)
        )

        # -----------------------------------------------------
        # Average Return
        # -----------------------------------------------------

        if number_of_returns > 0:

            average_return = (
                total_return_amount
                / number_of_returns
            )

        else:

            average_return = Decimal("0")

        self._average_return_label.setText(
            self._format_money(
                average_return
            )
        )

        # -----------------------------------------------------
        # Return Rate
        # -----------------------------------------------------

        if number_of_sales > 0:

            return_rate = (
                Decimal(number_of_returns)
                / Decimal(number_of_sales)
                * Decimal("100")
            )

        else:

            return_rate = Decimal("0")

        self._return_rate_label.setText(
            f"{return_rate:.2f}%"
        )

        # -----------------------------------------------------
        # Returned Items Rate
        # -----------------------------------------------------

        if total_items_sold > 0:

            returned_items_rate = (
                Decimal(total_items_returned)
                / Decimal(total_items_sold)
                * Decimal("100")
            )

        else:

            returned_items_rate = Decimal("0")

        self._returned_items_rate_label.setText(
            f"{returned_items_rate:.2f}%"
        )

        # -----------------------------------------------------
        # Information
        # -----------------------------------------------------

        self._information_label.setText(
            f"During the selected period, "
            f"{number_of_returns} return(s) were recorded, "
            f"representing "
            f"{self._format_money(total_return_amount)} "
            f"in returned sales and "
            f"{total_items_returned} item(s) returned."
        )

    # ---------------------------------------------------------
    # Backward-compatible service loader
    # ---------------------------------------------------------

    def load_report(
        self,
        *,
        start_date,
        end_date,
        number_of_sales: int = 0,
        total_items_sold: int = 0,
    ) -> None:

        returns = (
            self._report_service.get_sales_return_summary(
                start_date=start_date,
                end_date=end_date,
            )
        )

        self.set_data(
            returns,
            number_of_sales=number_of_sales,
            total_items_sold=total_items_sold,
        )

    # =========================================================
    # UI HELPERS
    # =========================================================

    @staticmethod
    def _create_value_label(
        value: str,
    ) -> QLabel:

        label = QLabel(value)

        label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        return label

    @staticmethod
    def _add_metric(
        layout: QGridLayout,
        row: int,
        column: int,
        title: str,
        value_label: QLabel,
    ) -> None:

        container = QWidget()

        container_layout = QVBoxLayout(
            container
        )

        container_layout.setContentsMargins(
            8,
            4,
            8,
            4,
        )

        container_layout.setSpacing(
            4
        )

        title_label = QLabel(title)

        value_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )

        value_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        container_layout.addWidget(
            title_label
        )

        container_layout.addWidget(
            value_label
        )

        layout.addWidget(
            container,
            row,
            column,
        )

        layout.setColumnStretch(
            column,
            1,
        )

    @staticmethod
    def _format_money(
        value: Decimal,
    ) -> str:

        return f"₦{value:,.2f}"