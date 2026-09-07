from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QGridLayout,
    QGroupBox,
    QHeaderView,
    QLabel,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.models.stock_movement import (
    StockMovement,
)


class StockMovementReport(QWidget):

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

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            16,
            16,
            16,
            16,
        )

        main_layout.setSpacing(
            16,
        )

        # -----------------------------------------------------
        # Movement Summary
        # -----------------------------------------------------

        movement_group = QGroupBox(
            "Stock Movement Summary"
        )

        movement_layout = QGridLayout()

        movement_layout.setHorizontalSpacing(
            16
        )

        movement_layout.setVerticalSpacing(
            16
        )

        self._movements_count_label = (
            self._create_value_label("0")
        )

        self._purchased_quantity_label = (
            self._create_value_label("0")
        )

        self._sold_quantity_label = (
            self._create_value_label("0")
        )

        self._sales_returned_quantity_label = (
            self._create_value_label("0")
        )

        self._damaged_quantity_label = (
            self._create_value_label("0")
        )

        self._supplier_returned_quantity_label = (
            self._create_value_label("0")
        )

        self._adjustment_in_label = (
            self._create_value_label("0")
        )

        self._adjustment_out_label = (
            self._create_value_label("0")
        )

        self._returned_in_label = (
            self._create_value_label("0")
        )

        self._add_metric(
            movement_layout,
            0,
            0,
            "Total Movements",
            self._movements_count_label,
        )

        self._add_metric(
            movement_layout,
            0,
            1,
            "Purchased",
            self._purchased_quantity_label,
        )

        self._add_metric(
            movement_layout,
            0,
            2,
            "Sold",
            self._sold_quantity_label,
        )

        self._add_metric(
            movement_layout,
            1,
            0,
            "Sales Returned",
            self._sales_returned_quantity_label,
        )

        self._add_metric(
            movement_layout,
            1,
            1,
            "Damaged",
            self._damaged_quantity_label,
        )

        self._add_metric(
            movement_layout,
            1,
            2,
            "Returned to Supplier",
            self._supplier_returned_quantity_label,
        )

        self._add_metric(
            movement_layout,
            2,
            0,
            "Adjustment In",
            self._adjustment_in_label,
        )

        self._add_metric(
            movement_layout,
            2,
            1,
            "Adjustment Out",
            self._adjustment_out_label,
        )

        self._add_metric(
            movement_layout,
            2,
            2,
            "Return In",
            self._returned_in_label,
        )

        movement_group.setLayout(
            movement_layout
        )

        main_layout.addWidget(
            movement_group
        )

        # -----------------------------------------------------
        # Movement History
        # -----------------------------------------------------

        history_group = QGroupBox(
            "Stock Movement History"
        )

        history_layout = QVBoxLayout()

        self._movement_table = QTableWidget()

        self._movement_table.setColumnCount(
            7
        )

        self._movement_table.setHorizontalHeaderLabels(
            [
                "Date",
                "Product",
                "Variant",
                "Movement",
                "Quantity",
                "Reference",
                "Notes",
            ]
        )

        self._movement_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        self._movement_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )

        self._movement_table.setSelectionMode(
            QTableWidget.SelectionMode.SingleSelection
        )

        self._movement_table.setAlternatingRowColors(
            True
        )

        self._movement_table.verticalHeader().setVisible(
            False
        )

        self._movement_table.setWordWrap(
            True
        )

        self._movement_table.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        header = (
            self._movement_table.horizontalHeader()
        )

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        # Make the first columns slightly more useful.
        header.setMinimumSectionSize(
            80
        )

        history_layout.addWidget(
            self._movement_table
        )

        history_group.setLayout(
            history_layout
        )

        main_layout.addWidget(
            history_group,
            1,
        )

    # =========================================================
    # DATA
    # =========================================================

    def set_data(
        self,
        *,
        movements,
        history: list[StockMovement],
    ) -> None:

        # -----------------------------------------------------
        # Summary
        # -----------------------------------------------------

        self._movements_count_label.setText(
            str(
                movements.total_movements
            )
        )

        self._purchased_quantity_label.setText(
            str(
                movements.total_purchased
            )
        )

        self._sold_quantity_label.setText(
            str(
                movements.total_sold
            )
        )

        self._sales_returned_quantity_label.setText(
            str(
                movements.total_sales_returned
            )
        )

        self._damaged_quantity_label.setText(
            str(
                movements.total_damaged
            )
        )

        self._supplier_returned_quantity_label.setText(
            str(
                movements.total_returned_to_supplier
            )
        )

        self._adjustment_in_label.setText(
            str(
                movements.total_adjustment_in
            )
        )

        self._adjustment_out_label.setText(
            str(
                movements.total_adjustment_out
            )
        )

        self._returned_in_label.setText(
            str(
                movements.total_returned_in
            )
        )

        # -----------------------------------------------------
        # History
        # -----------------------------------------------------

        self._load_movement_table(
            history
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

        movements = (
            self._report_service
            .get_stock_movement_summary(
                start_date=start_date,
                end_date=end_date,
            )
        )

        history = (
            self._report_service
            .get_stock_movement_history(
                start_date=start_date,
                end_date=end_date,
            )
        )

        self.set_data(
            movements=movements,
            history=history,
        )

    # =========================================================
    # TABLE
    # =========================================================

    def _load_movement_table(
        self,
        movements: list[StockMovement],
    ) -> None:

        self._movement_table.clearContents()

        self._movement_table.setRowCount(
            len(movements)
        )

        for row, movement in enumerate(
            movements
        ):

            variant = movement.variant

            product_name = (
                variant.product.name
                if variant
                and variant.product
                else "Unknown"
            )

            # -------------------------------------------------
            # Variant
            # -------------------------------------------------

            if variant is not None:

                if variant.sku:

                    variant_name = (
                        variant.sku
                    )

                else:

                    variant_name = (
                        f"{variant.length} yards"
                    )

            else:

                variant_name = ""

            # -------------------------------------------------
            # Values
            # -------------------------------------------------

            created_at = movement.created_at

            if created_at is not None:

                date_text = (
                    created_at.strftime(
                        "%Y-%m-%d %H:%M"
                    )
                )

            else:

                date_text = ""

            movement_type = (
                movement.movement_type.value
            )

            values = [
                date_text,
                product_name,
                variant_name,
                movement_type,
                str(
                    movement.quantity
                ),
                movement.reference or "",
                movement.notes or "",
            ]

            # -------------------------------------------------
            # Table cells
            # -------------------------------------------------

            for column, value in enumerate(
                values
            ):

                item = QTableWidgetItem(
                    value
                )

                item.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft
                    | Qt.AlignmentFlag.AlignVCenter
                )

                item.setToolTip(
                    value
                )

                self._movement_table.setItem(
                    row,
                    column,
                    item,
                )

        self._movement_table.resizeRowsToContents()

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
            8,
            8,
            8,
        )

        container_layout.setSpacing(
            4
        )

        title_label = QLabel(title)

        title_label.setWordWrap(
            True
        )

        value_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
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