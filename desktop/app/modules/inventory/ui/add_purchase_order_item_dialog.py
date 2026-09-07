from __future__ import annotations

from decimal import Decimal

from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QSpinBox,
    QVBoxLayout,
)


class AddPurchaseOrderItemDialog(QDialog):

    def __init__(
        self,
        variant_service,
        parent=None,
    ) -> None:
        super().__init__(parent)

        self._variant_service = variant_service

        self._build_ui()
        self._load_variants()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Purchase Order Item"
        )

        self.setMinimumSize(
            500,
            300,
        )

        self.resize(
            550,
            320,
        )

        # -----------------------------------------------------
        # Title
        # -----------------------------------------------------

        title = QLabel(
            "Purchase Order Item"
        )

        title.setObjectName(
            "dialogTitle"
        )

        # -----------------------------------------------------
        # Form group
        # -----------------------------------------------------

        form_group = QGroupBox(
            "Item Information"
        )

        form_layout = QFormLayout()

        form_layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        form_layout.setSpacing(
            12
        )

        # -----------------------------------------------------
        # Variant
        # -----------------------------------------------------

        self.variant_combo = QComboBox()

        self.variant_combo.setMinimumHeight(
            36
        )

        self.variant_combo.setMinimumWidth(
            300
        )

        self.variant_combo.currentIndexChanged.connect(
            self._variant_changed
        )

        # -----------------------------------------------------
        # Quantity
        # -----------------------------------------------------

        self.quantity_spin = QSpinBox()

        self.quantity_spin.setMinimum(
            1
        )

        self.quantity_spin.setMaximum(
            1_000_000
        )

        self.quantity_spin.setValue(
            1
        )

        self.quantity_spin.setMinimumHeight(
            36
        )

        # -----------------------------------------------------
        # Cost price
        # -----------------------------------------------------

        self.cost_price_spin = QDoubleSpinBox()

        self.cost_price_spin.setReadOnly(
            True
        )

        self.cost_price_spin.setMinimum(
            0
        )

        self.cost_price_spin.setMaximum(
            1_000_000
        )

        self.cost_price_spin.setDecimals(
            2
        )

        self.cost_price_spin.setMinimumHeight(
            36
        )

        # Prevent the user from changing the
        # automatically loaded cost price.
        self.cost_price_spin.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        # -----------------------------------------------------
        # Add fields
        # -----------------------------------------------------

        form_layout.addRow(
            "Variant:",
            self.variant_combo,
        )

        form_layout.addRow(
            "Quantity:",
            self.quantity_spin,
        )

        form_layout.addRow(
            "Cost Price:",
            self.cost_price_spin,
        )

        form_group.setLayout(
            form_layout
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok
            | QDialogButtonBox.StandardButton.Cancel
        )

        self.buttons.setMinimumHeight(
            40
        )

        self.buttons.accepted.connect(
            self._accept
        )

        self.buttons.rejected.connect(
            self.reject
        )

        # -----------------------------------------------------
        # Main layout
        # -----------------------------------------------------

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        main_layout.setSpacing(
            15
        )

        main_layout.addWidget(
            title
        )

        main_layout.addWidget(
            form_group
        )

        main_layout.addStretch()

        main_layout.addWidget(
            self.buttons
        )

    # =========================================================
    # DATA
    # =========================================================

    def _load_variants(self) -> None:

        self.variant_combo.clear()

        variants = (
            self._variant_service.get_all()
        )

        ok_button = self.buttons.button(
            QDialogButtonBox.StandardButton.Ok
        )

        if not variants:

            self.variant_combo.addItem(
                "No variants available",
                None,
            )

            ok_button.setEnabled(
                False
            )

            return

        ok_button.setEnabled(
            True
        )

        for variant in variants:

            product_name = (
                variant.product.name
                if variant.product
                else ""
            )

            length = (
                str(variant.length)
                if variant.length is not None
                else ""
            )

            if variant.sku:

                text = (
                    f"{product_name} - "
                    f"{variant.sku} - "
                    f"{length}"
                )

            else:

                text = (
                    f"{product_name} - "
                    f"{length}"
                )

            self.variant_combo.addItem(
                text,
                variant.id,
            )

        self._variant_changed()

    # =========================================================
    # VALUES
    # =========================================================

    def values(self) -> dict:

        return {
            "variant_id": (
                self.variant_combo.currentData()
            ),
            "quantity": (
                self.quantity_spin.value()
            ),
            "cost_price": Decimal(
                str(
                    self.cost_price_spin.value()
                )
            ),
        }

    # =========================================================
    # VARIANT
    # =========================================================

    def _variant_changed(
        self,
        index: int = -1,
    ) -> None:

        variant_id = (
            self.variant_combo.currentData()
        )

        if variant_id is None:

            self.cost_price_spin.setValue(
                0
            )

            return

        variant = (
            self._variant_service.get_by_id(
                variant_id
            )
        )

        if variant is None:

            self.cost_price_spin.setValue(
                0
            )

            return

        self.cost_price_spin.setValue(
            float(
                variant.cost_price
            )
        )

    # =========================================================
    # ACCEPT
    # =========================================================

    def _accept(self) -> None:

        if (
            self.variant_combo.currentData()
            is None
        ):
            return

        if (
            self.quantity_spin.value()
            <= 0
        ):
            return

        self.accept()