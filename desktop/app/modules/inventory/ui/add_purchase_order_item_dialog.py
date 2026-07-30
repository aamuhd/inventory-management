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
        self.variant_combo.currentIndexChanged.connect(
            self._variant_changed,
        )

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)

        self.cost_price_spin = QDoubleSpinBox()
        self.cost_price_spin.setReadOnly(
            True,
        )
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
        """
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        """
        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )
        """
        self.buttons.accepted.connect(
            self.accept,
        )
        """
        self.buttons.accepted.connect(
            self._accept,
        )

        self.buttons.rejected.connect(
            self.reject,
        )

        layout.addWidget(
            self.buttons,
        )

    def _load_variants(self):

        self.variant_combo.clear()
        variants = self._variant_service.get_all()

        if not variants:
            self.variant_combo.addItem(
                "No variants available",
                None,
            )
            self.buttons.button(
                QDialogButtonBox.StandardButton.Ok,
            ).setEnabled(False)

            return
        self.buttons.button(
            QDialogButtonBox.StandardButton.Ok,
        ).setEnabled(True)
        for variant in variants:
            text = (
                f"{variant.product.name}"
                f" - {variant.length}"
            )
            self.variant_combo.addItem(
                text,
                variant.id,
            )
        self._variant_changed()

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
    
    def _variant_changed(self):

        variant_id = self.variant_combo.currentData()
        if variant_id is None:
            self.cost_price_spin.setValue(
                0,
            )

            return

        variant = self._variant_service.get_by_id(
            variant_id,
        )
        self.cost_price_spin.setValue(
            float(
                variant.cost_price,
            )
        )

    def _accept(self):

        if self.variant_combo.currentData() is None:
            return
        self.accept()