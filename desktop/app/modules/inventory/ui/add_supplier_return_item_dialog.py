from decimal import Decimal
from uuid import UUID

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QVBoxLayout,
)

from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)


class AddSupplierReturnItemDialog(QDialog):

    def __init__(
        self,
        variant_service: ProductVariantService,
        parent=None,
    ):

        super().__init__(parent)

        self._variant_service = variant_service

        self.setWindowTitle(
            "Add Supplier Return Item",
        )

        self._build_ui()

        self._load_variants()

    def _build_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.variant_combo = QComboBox()

        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)

        self.unit_cost_spin = QDoubleSpinBox()
        self.unit_cost_spin.setDecimals(2)
        self.unit_cost_spin.setMaximum(999999999)

        self.reason_edit = QLineEdit()

        form.addRow(
            "Variant",
            self.variant_combo,
        )

        form.addRow(
            "Quantity",
            self.quantity_spin,
        )

        form.addRow(
            "Unit Cost",
            self.unit_cost_spin,
        )

        form.addRow(
            "Reason",
            self.reason_edit,
        )

        layout.addLayout(form)

        self.button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        layout.addWidget(
            self.button_box,
        )

        self.button_box.accepted.connect(
            self._accept,
        )

        self.button_box.rejected.connect(
            self.reject,
        )

    def _load_variants(self):

        self.variant_combo.clear()

        variants = self._variant_service.get_all()

        for variant in variants:

            if variant.sku:
                text = variant.sku
            else:
                text = (
                    f"{variant.product.name}"
                    f" ({variant.length})"
                )

            self.variant_combo.addItem(
                text,
                variant.id,
            )

    def _accept(self):

        if self.variant_combo.currentIndex() < 0:

            QMessageBox.warning(
                self,
                "Validation",
                "Please select a variant.",
            )

            return

        self.accept()

    def values(self):

        return {
            "variant_id": self.variant_combo.currentData(),
            "quantity": self.quantity_spin.value(),
            "unit_cost": Decimal(
                str(
                    self.unit_cost_spin.value(),
                )
            ),
            "reason": self.reason_edit.text().strip(),
        }

    def load_item(
        self,
        *,
        variant_id: UUID,
        quantity: int,
        reason: str,
    ):

        index = self.variant_combo.findData(
            variant_id,
        )

        self.variant_combo.setCurrentIndex(
            index,
        )

        self.quantity_spin.setValue(
            quantity,
        )

        self.reason_edit.setText(
            reason,
        )