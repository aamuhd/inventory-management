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


class PurchasesReport(QWidget):

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
        # Purchase Overview
        # -----------------------------------------------------

        overview_group = QGroupBox(
            "Purchase Overview"
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

        self._purchase_orders_label = (
            self._create_value_label("0")
        )

        self._purchase_amount_label = (
            self._create_value_label("₹0.00")
        )

        self._items_ordered_label = (
            self._create_value_label("0")
        )

        self._items_received_label = (
            self._create_value_label("0")
        )

        self._add_metric(
            overview_layout,
            0,
            0,
            "Number of Orders",
            self._purchase_orders_label,
        )

        self._add_metric(
            overview_layout,
            0,
            1,
            "Purchase Amount",
            self._purchase_amount_label,
        )

        self._add_metric(
            overview_layout,
            1,
            0,
            "Items Ordered",
            self._items_ordered_label,
        )

        self._add_metric(
            overview_layout,
            1,
            1,
            "Items Received",
            self._items_received_label,
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
        # Purchase Analysis
        # -----------------------------------------------------

        analysis_group = QGroupBox(
            "Purchase Analysis"
        )

        analysis_layout = QGridLayout()

        analysis_layout.setHorizontalSpacing(
            16
        )

        analysis_layout.setVerticalSpacing(
            12
        )

        self._average_order_value_label = (
            self._create_value_label("₹0.00")
        )

        self._items_received_rate_label = (
            self._create_value_label("0.00%")
        )

        self._items_pending_label = (
            self._create_value_label("0")
        )

        analysis_layout.addWidget(
            QLabel("Average Order Value"),
            0,
            0,
        )

        analysis_layout.addWidget(
            self._average_order_value_label,
            0,
            1,
        )

        analysis_layout.addWidget(
            QLabel("Items Received Rate"),
            1,
            0,
        )

        analysis_layout.addWidget(
            self._items_received_rate_label,
            1,
            1,
        )

        analysis_layout.addWidget(
            QLabel("Items Pending"),
            2,
            0,
        )

        analysis_layout.addWidget(
            self._items_pending_label,
            2,
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
            "Purchase Information"
        )

        information_layout = QVBoxLayout()

        self._information_label = QLabel(
            "Purchase information for the selected period."
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
        purchases,
    ) -> None:

        number_of_orders = (
            purchases.number_of_orders
        )

        total_purchase_amount = (
            purchases.total_purchase_amount
        )

        total_items_ordered = (
            purchases.total_items_ordered
        )

        total_items_received = (
            purchases.total_items_received
        )

        # -----------------------------------------------------
        # Overview
        # -----------------------------------------------------

        self._purchase_orders_label.setText(
            str(number_of_orders)
        )

        self._purchase_amount_label.setText(
            self._format_money(
                total_purchase_amount
            )
        )

        self._items_ordered_label.setText(
            str(total_items_ordered)
        )

        self._items_received_label.setText(
            str(total_items_received)
        )

        # -----------------------------------------------------
        # Average Order Value
        # -----------------------------------------------------

        if number_of_orders > 0:

            average_order_value = (
                total_purchase_amount
                / number_of_orders
            )

        else:

            average_order_value = Decimal("0")

        self._average_order_value_label.setText(
            self._format_money(
                average_order_value
            )
        )

        # -----------------------------------------------------
        # Items Received Rate
        # -----------------------------------------------------

        if total_items_ordered > 0:

            received_rate = (
                Decimal(total_items_received)
                / Decimal(total_items_ordered)
                * Decimal("100")
            )

        else:

            received_rate = Decimal("0")

        self._items_received_rate_label.setText(
            f"{received_rate:.2f}%"
        )

        # -----------------------------------------------------
        # Items Pending
        # -----------------------------------------------------

        items_pending = max(
            total_items_ordered
            - total_items_received,
            0,
        )

        self._items_pending_label.setText(
            str(items_pending)
        )

        # -----------------------------------------------------
        # Information
        # -----------------------------------------------------

        self._information_label.setText(
            f"During the selected period, "
            f"{number_of_orders} purchase order(s) "
            f"were recorded with a total purchase value "
            f"of {self._format_money(total_purchase_amount)}. "
            f"{total_items_received} of "
            f"{total_items_ordered} ordered item(s) "
            f"have been received."
        )

    # ---------------------------------------------------------
    # Backward-compatible service loader
    # ---------------------------------------------------------

    def load_report(
        self,
        *,
        start_date,
        end_date,
    ) -> None:

        purchases = (
            self._report_service.get_purchase_summary(
                start_date=start_date,
                end_date=end_date,
            )
        )

        self.set_data(
            purchases
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



#₦
