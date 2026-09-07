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


class OverviewReport(QWidget):

    def __init__(self) -> None:
        super().__init__()

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

        main_layout.setSpacing(12)

        # -----------------------------------------------------
        # Sales
        # -----------------------------------------------------

        sales_group = QGroupBox("Sales")

        sales_layout = QGridLayout()

        sales_layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        sales_layout.setHorizontalSpacing(16)
        sales_layout.setVerticalSpacing(4)

        self._total_sales_label = self._create_value_label(
            "₦0.00"
        )

        self._number_of_sales_label = self._create_value_label(
            "0"
        )

        self._items_sold_label = self._create_value_label(
            "0"
        )

        self._average_sale_label = self._create_value_label(
            "₦0.00"
        )

        self._add_metric(
            sales_layout,
            0,
            0,
            "Total Sales",
            self._total_sales_label,
        )

        self._add_metric(
            sales_layout,
            0,
            1,
            "Number of Sales",
            self._number_of_sales_label,
        )

        self._add_metric(
            sales_layout,
            1,
            0,
            "Items Sold",
            self._items_sold_label,
        )

        self._add_metric(
            sales_layout,
            1,
            1,
            "Average Sale",
            self._average_sale_label,
        )

        sales_group.setLayout(
            sales_layout
        )

        main_layout.addWidget(
            sales_group
        )

        # -----------------------------------------------------
        # Inventory
        # -----------------------------------------------------

        inventory_group = QGroupBox("Inventory")

        inventory_layout = QGridLayout()

        inventory_layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        inventory_layout.setHorizontalSpacing(16)
        inventory_layout.setVerticalSpacing(4)

        self._total_variants_label = self._create_value_label(
            "0"
        )

        self._stock_quantity_label = self._create_value_label(
            "0"
        )

        self._inventory_cost_label = self._create_value_label(
            "₦0.00"
        )

        self._inventory_selling_label = self._create_value_label(
            "₦0.00"
        )

        self._low_stock_label = self._create_value_label(
            "0"
        )

        self._add_metric(
            inventory_layout,
            0,
            0,
            "Total Variants",
            self._total_variants_label,
        )

        self._add_metric(
            inventory_layout,
            0,
            1,
            "Total Stock",
            self._stock_quantity_label,
        )

        self._add_metric(
            inventory_layout,
            1,
            0,
            "Inventory Cost",
            self._inventory_cost_label,
        )

        self._add_metric(
            inventory_layout,
            1,
            1,
            "Inventory Selling Value",
            self._inventory_selling_label,
        )

        self._add_metric(
            inventory_layout,
            2,
            0,
            "Low Stock",
            self._low_stock_label,
        )

        inventory_group.setLayout(
            inventory_layout
        )

        main_layout.addWidget(
            inventory_group
        )

        # -----------------------------------------------------
        # Purchases
        # -----------------------------------------------------

        purchase_group = QGroupBox("Purchases")

        purchase_layout = QGridLayout()

        purchase_layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        purchase_layout.setHorizontalSpacing(16)
        purchase_layout.setVerticalSpacing(4)

        self._purchase_orders_label = self._create_value_label(
            "0"
        )

        self._purchase_amount_label = self._create_value_label(
            "₦0.00"
        )

        self._items_ordered_label = self._create_value_label(
            "0"
        )

        self._items_received_label = self._create_value_label(
            "0"
        )

        self._add_metric(
            purchase_layout,
            0,
            0,
            "Number of Orders",
            self._purchase_orders_label,
        )

        self._add_metric(
            purchase_layout,
            0,
            1,
            "Purchase Amount",
            self._purchase_amount_label,
        )

        self._add_metric(
            purchase_layout,
            1,
            0,
            "Items Ordered",
            self._items_ordered_label,
        )

        self._add_metric(
            purchase_layout,
            1,
            1,
            "Items Received",
            self._items_received_label,
        )

        purchase_group.setLayout(
            purchase_layout
        )

        main_layout.addWidget(
            purchase_group
        )

        # -----------------------------------------------------
        # Sales Returns
        # -----------------------------------------------------

        returns_group = QGroupBox(
            "Sales Returns"
        )

        returns_layout = QGridLayout()

        returns_layout.setContentsMargins(
            8,
            8,
            8,
            8,
        )

        returns_layout.setHorizontalSpacing(16)
        returns_layout.setVerticalSpacing(4)

        self._returns_count_label = self._create_value_label(
            "0"
        )

        self._returns_amount_label = self._create_value_label(
            "₦0.00"
        )

        self._returned_items_label = self._create_value_label(
            "0"
        )

        self._add_metric(
            returns_layout,
            0,
            0,
            "Number of Returns",
            self._returns_count_label,
        )

        self._add_metric(
            returns_layout,
            0,
            1,
            "Return Amount",
            self._returns_amount_label,
        )

        self._add_metric(
            returns_layout,
            1,
            0,
            "Items Returned",
            self._returned_items_label,
        )

        returns_group.setLayout(
            returns_layout
        )

        main_layout.addWidget(
            returns_group
        )

        # Keep some space below the final section.
        main_layout.addStretch()

        scroll_area.setWidget(
            content
        )

        outer_layout.addWidget(
            scroll_area
        )

    # =========================================================
    # METRIC HELPERS
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

        group = QWidget()

        group_layout = QGridLayout(group)

        group_layout.setContentsMargins(
            8,
            4,
            8,
            4,
        )

        group_layout.setHorizontalSpacing(
            8
        )

        title_label = QLabel(
            title
        )

        title_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        value_label.setMinimumWidth(
            100
        )

        group_layout.addWidget(
            title_label,
            0,
            0,
        )

        group_layout.addWidget(
            value_label,
            0,
            1,
        )

        group_layout.setColumnStretch(
            0,
            1,
        )

        group_layout.setColumnStretch(
            1,
            0,
        )

        layout.addWidget(
            group,
            row,
            column,
        )

        layout.setColumnStretch(
            column,
            1,
        )

    # =========================================================
    # DATA
    # =========================================================

    def set_data(
        self,
        *,
        sales,
        inventory,
        purchases,
        returns,
        movements=None,
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

        self._total_variants_label.setText(
            str(
                inventory.total_variants
            )
        )

        self._stock_quantity_label.setText(
            str(
                inventory.total_stock_quantity
            )
        )

        self._inventory_cost_label.setText(
            self._format_money(
                inventory.inventory_cost_value
            )
        )

        self._inventory_selling_label.setText(
            self._format_money(
                inventory.inventory_selling_value
            )
        )

        self._low_stock_label.setText(
            str(
                inventory.low_stock_count
            )
        )

        self._purchase_orders_label.setText(
            str(
                purchases.number_of_orders
            )
        )

        self._purchase_amount_label.setText(
            self._format_money(
                purchases.total_purchase_amount
            )
        )

        self._items_ordered_label.setText(
            str(
                purchases.total_items_ordered
            )
        )

        self._items_received_label.setText(
            str(
                purchases.total_items_received
            )
        )

        self._returns_count_label.setText(
            str(
                returns.number_of_returns
            )
        )

        self._returns_amount_label.setText(
            self._format_money(
                returns.total_return_amount
            )
        )

        self._returned_items_label.setText(
            str(
                returns.total_items_returned
            )
        )

    # =========================================================
    # HELPERS
    # =========================================================

    @staticmethod
    def _format_money(
        value: Decimal,
    ) -> str:

        return f"₦{value:,.2f}" 