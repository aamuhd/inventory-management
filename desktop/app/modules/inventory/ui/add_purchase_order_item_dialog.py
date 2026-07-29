from decimal import Decimal

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QSpinBox,
)


class AddPurchaseOrderItemDialog(QDialog):

    def __init__(
        self,
        variant_service,
        parent=None,
    ):
        super().__init__(parent)

        self._variant_service = variant_service

        self._build_ui()
        self._load_variants()

    def _build_ui(self):

        self.setWindowTitle(
            "Purchase Order Item",
        )

        layout = QFormLayout(self)

        self.variant_combo = QComboBox()

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)

        self.cost_price_spin = QDoubleSpinBox()
        self.cost_price_spin.setMinimum(0)
        self.cost_price_spin.setMaximum(1_000_000)
        self.cost_price_spin.setDecimals(2)

        layout.addRow(
            "Variant",
            self.variant_combo,
        )

        layout.addRow(
            "Quantity",
            self.quantity_spin,
        )

        layout.addRow(
            "Cost Price",
            self.cost_price_spin,
        )

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        buttons.accepted.connect(
            self.accept,
        )

        buttons.rejected.connect(
            self.reject,
        )

        layout.addWidget(
            buttons,
        )

    def _load_variants(self):

        variants = self._variant_service.get_all()

        for variant in variants:

            text = (
                f"{variant.product.name}"
                f" - {variant.length}"
            )

            self.variant_combo.addItem(
                text,
                variant.id,
            )

    def values(self):

        return {
            "variant_id": self.variant_combo.currentData(),
            "quantity": self.quantity_spin.value(),
            "cost_price": Decimal(
                str(
                    self.cost_price_spin.value(),
                )
            ),
        }