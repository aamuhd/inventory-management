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

#₦

class InventoryReport(QWidget):

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
        # Scroll area
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
        # Inventory Overview
        # -----------------------------------------------------

        overview_group = QGroupBox(
            "Inventory Overview"
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

        self._total_variants_label = (
            self._create_value_label("0")
        )

        self._stock_quantity_label = (
            self._create_value_label("0")
        )

        self._low_stock_label = (
            self._create_value_label("0")
        )

        self._add_metric(
            overview_layout,
            0,
            0,
            "Total Variants",
            self._total_variants_label,
        )

        self._add_metric(
            overview_layout,
            0,
            1,
            "Total Stock Quantity",
            self._stock_quantity_label,
        )

        self._add_metric(
            overview_layout,
            0,
            2,
            "Low Stock Variants",
            self._low_stock_label,
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

        main_layout.addWidget(
            overview_group
        )

        # -----------------------------------------------------
        # Inventory Valuation
        # -----------------------------------------------------

        value_group = QGroupBox(
            "Inventory Valuation"
        )

        value_layout = QGridLayout()

        value_layout.setHorizontalSpacing(
            16
        )

        value_layout.setVerticalSpacing(
            8
        )

        self._cost_value_label = (
            self._create_value_label("₦0.00")
        )

        self._selling_value_label = (
            self._create_value_label("₦0.00")
        )

        self._potential_profit_label = (
            self._create_value_label("₦0.00")
        )

        self._add_simple_metric(
            value_layout,
            0,
            "Cost Value",
            self._cost_value_label,
        )

        self._add_simple_metric(
            value_layout,
            1,
            "Selling Value",
            self._selling_value_label,
        )

        self._add_simple_metric(
            value_layout,
            2,
            "Potential Gross Profit",
            self._potential_profit_label,
        )

        value_group.setLayout(
            value_layout
        )

        main_layout.addWidget(
            value_group
        )

        # -----------------------------------------------------
        # Stock Status
        # -----------------------------------------------------

        status_group = QGroupBox(
            "Stock Status"
        )

        status_layout = QGridLayout()

        status_layout.setHorizontalSpacing(
            16
        )

        status_layout.setVerticalSpacing(
            8
        )

        self._healthy_stock_label = (
            self._create_value_label("0")
        )

        self._low_stock_status_label = (
            self._create_value_label("0")
        )

        self._stock_health_label = (
            self._create_value_label("0.00%")
        )

        self._add_simple_metric(
            status_layout,
            0,
            "Healthy Stock Variants",
            self._healthy_stock_label,
        )

        self._add_simple_metric(
            status_layout,
            1,
            "Low Stock Variants",
            self._low_stock_status_label,
        )

        self._add_simple_metric(
            status_layout,
            2,
            "Stock Health",
            self._stock_health_label,
        )

        status_group.setLayout(
            status_layout
        )

        main_layout.addWidget(
            status_group
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
        inventory,
    ) -> None:

        total_variants = (
            inventory.total_variants
        )

        total_stock_quantity = (
            inventory.total_stock_quantity
        )

        inventory_cost_value = (
            inventory.inventory_cost_value
        )

        inventory_selling_value = (
            inventory.inventory_selling_value
        )

        low_stock_count = (
            inventory.low_stock_count
        )

        # -----------------------------------------------------
        # Inventory Overview
        # -----------------------------------------------------

        self._total_variants_label.setText(
            str(total_variants)
        )

        self._stock_quantity_label.setText(
            str(total_stock_quantity)
        )

        self._low_stock_label.setText(
            str(low_stock_count)
        )

        # -----------------------------------------------------
        # Valuation
        # -----------------------------------------------------

        self._cost_value_label.setText(
            self._format_money(
                inventory_cost_value
            )
        )

        self._selling_value_label.setText(
            self._format_money(
                inventory_selling_value
            )
        )

        potential_profit = (
            inventory_selling_value
            - inventory_cost_value
        )

        self._potential_profit_label.setText(
            self._format_money(
                potential_profit
            )
        )

        # -----------------------------------------------------
        # Stock Status
        # -----------------------------------------------------

        self._low_stock_status_label.setText(
            str(low_stock_count)
        )

        healthy_stock = max(
            total_variants - low_stock_count,
            0,
        )

        self._healthy_stock_label.setText(
            str(healthy_stock)
        )

        if total_variants > 0:

            stock_health = (
                Decimal(healthy_stock)
                / Decimal(total_variants)
                * Decimal("100")
            )

        else:

            stock_health = Decimal("0")

        self._stock_health_label.setText(
            f"{stock_health:.2f}%"
        )
    # =========================================================
    # BACKWARD-COMPATIBLE SERVICE LOADER
    # =========================================================

    def load_report(self) -> None:

        inventory = (
            self._report_service.get_inventory_summary()
        )

        self.set_data(
            inventory
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
    def _add_simple_metric(
        layout: QGridLayout,
        row: int,
        title: str,
        value_label: QLabel,
    ) -> None:

        title_label = QLabel(title)

        layout.addWidget(
            title_label,
            row,
            0,
        )

        layout.addWidget(
            value_label,
            row,
            1,
        )

        layout.setColumnStretch(
            1,
            1,
        )

    @staticmethod
    def _format_money(
        value: Decimal,
    ) -> str:

        return f"₦{value:,.2f}"
    