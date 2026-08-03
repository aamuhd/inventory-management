from decimal import Decimal

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QSpinBox,
)

from app.modules.sales.services.sale_service import SaleService


class AddSaleItemDialog(QDialog):

    def __init__(
        self,
        variant_service,
        parent=None,
    ):
        super().__init__(parent)

        self._variant_service = variant_service

        self._variants = []

        self._build_ui()
        self._load_variants()
        self._connect_signals()

    def _build_ui(self):

        self.setWindowTitle(
            "Sale Item",
        )

        layout = QFormLayout(self)

        self.variant_combo = QComboBox()

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)

        self.unit_price_spin = QDoubleSpinBox()
        self.unit_price_spin.setMinimum(0)
        self.unit_price_spin.setMaximum(1_000_000)
        self.unit_price_spin.setDecimals(2)

        layout.addRow(
            "Variant",
            self.variant_combo,
        )

        layout.addRow(
            "Quantity",
            self.quantity_spin,
        )

        layout.addRow(
            "Unit Price",
            self.unit_price_spin,
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

    def _connect_signals(self):

        self.variant_combo.currentIndexChanged.connect(
            self._variant_changed,
        )

    def _load_variants(self):

        self._variants = self._variant_service.get_all()

        for variant in self._variants:

            text = (
                f"{variant.product.name}"
                f" - {variant.length} yards"
            )

            self.variant_combo.addItem(
                text,
                variant.id,
            )

        self._variant_changed()

    def _variant_changed(self):

        index = self.variant_combo.currentIndex()

        if index < 0:
            return

        variant = self._variants[index]

        self.unit_price_spin.setValue(
            float(
                variant.selling_price,
            )
        )

    def values(self):

        return {
            "variant_id": self.variant_combo.currentData(),
            "quantity": self.quantity_spin.value(),
            "unit_price": Decimal(
                str(
                    self.unit_price_spin.value(),
                )
            ),
        }