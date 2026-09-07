from __future__ import annotations

from decimal import Decimal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.models.product import Product


class ProductVariantForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        title = QLabel(
            "Product Variant Information"
        )

        title.setObjectName(
            "productVariantFormTitle"
        )

        # -----------------------------------------------------
        # Product
        # -----------------------------------------------------

        self.product_combo = QComboBox()

        self.product_combo.setObjectName(
            "productVariantProductCombo"
        )

        self.product_combo.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Variant Name
        # -----------------------------------------------------

        self.name_input = QLineEdit()

        self.name_input.setObjectName(
            "productVariantNameInput"
        )

        self.name_input.setPlaceholderText(
            "Enter variant name"
        )

        self.name_input.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Length
        # -----------------------------------------------------

        self.length_input = QSpinBox()

        self.length_input.setObjectName(
            "productVariantLengthInput"
        )

        self.length_input.setRange(
            1,
            999999999,
        )

        self.length_input.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # SKU
        # -----------------------------------------------------

        self.sku_input = QLineEdit()

        self.sku_input.setObjectName(
            "productVariantSkuInput"
        )

        self.sku_input.setPlaceholderText(
            "Enter SKU"
        )

        self.sku_input.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Stock Quantity
        # -----------------------------------------------------

        self.stock_quantity_input = QSpinBox()

        self.stock_quantity_input.setObjectName(
            "productVariantStockInput"
        )

        self.stock_quantity_input.setRange(
            0,
            999999999,
        )

        self.stock_quantity_input.setValue(
            0
        )

        self.stock_quantity_input.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Reorder Level
        # -----------------------------------------------------

        self.reorder_level_input = QSpinBox()

        self.reorder_level_input.setObjectName(
            "productVariantReorderLevelInput"
        )

        self.reorder_level_input.setRange(
            0,
            999999999,
        )

        self.reorder_level_input.setValue(
            5
        )

        self.reorder_level_input.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Cost Price
        # -----------------------------------------------------

        self.cost_price_input = QDoubleSpinBox()

        self.cost_price_input.setObjectName(
            "productVariantCostPriceInput"
        )

        self.cost_price_input.setRange(
            0.00,
            999999999.99,
        )

        self.cost_price_input.setDecimals(
            2
        )

        self.cost_price_input.setValue(
            0.00
        )

        self.cost_price_input.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Selling Price
        # -----------------------------------------------------

        self.selling_price_input = QDoubleSpinBox()

        self.selling_price_input.setObjectName(
            "productVariantSellingPriceInput"
        )

        self.selling_price_input.setRange(
            0.00,
            999999999.99,
        )

        self.selling_price_input.setDecimals(
            2
        )

        self.selling_price_input.setValue(
            0.00
        )

        self.selling_price_input.setMinimumHeight(
            35
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        form_layout = QFormLayout()

        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        form_layout.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        form_layout.setVerticalSpacing(
            12
        )

        form_layout.addRow(
            "Product:",
            self.product_combo,
        )

        form_layout.addRow(
            "Variant Name:",
            self.name_input,
        )

        form_layout.addRow(
            "Length:",
            self.length_input,
        )

        form_layout.addRow(
            "SKU:",
            self.sku_input,
        )

        form_layout.addRow(
            "Stock Quantity:",
            self.stock_quantity_input,
        )

        form_layout.addRow(
            "Reorder Level:",
            self.reorder_level_input,
        )

        form_layout.addRow(
            "Cost Price:",
            self.cost_price_input,
        )

        form_layout.addRow(
            "Selling Price:",
            self.selling_price_input,
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.setObjectName(
            "productVariantSaveButton"
        )

        self.save_button.setMinimumHeight(
            38
        )

        self.save_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.clear_button = QPushButton(
            "Clear"
        )

        self.clear_button.setObjectName(
            "productVariantClearButton"
        )

        self.clear_button.setMinimumHeight(
            38
        )

        self.clear_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        # -----------------------------------------------------
        # Main Layout
        # -----------------------------------------------------

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            15,
            15,
            15,
            15,
        )

        layout.setSpacing(
            12
        )

        layout.addWidget(
            title
        )

        layout.addLayout(
            form_layout
        )

        layout.addStretch()

        layout.addLayout(
            button_layout
        )

    # =========================================================
    # PRODUCTS
    # =========================================================

    def load_products(
        self,
        products: list[Product],
    ) -> None:

        self.product_combo.clear()

        for product in products:

            self.product_combo.addItem(
                product.name,
                product.id,
            )

    # =========================================================
    # DATA
    # =========================================================

    def get_data(self) -> dict:

        return {
            "product_id": self.product_combo.currentData(),
            "name": self.name_input.text().strip(),
            "length": self.length_input.value(),
            "stock_quantity": self.stock_quantity_input.value(),
            "reorder_level": self.reorder_level_input.value(),
            "cost_price": Decimal(
                str(
                    self.cost_price_input.value()
                )
            ),
            "selling_price": Decimal(
                str(
                    self.selling_price_input.value()
                )
            ),
            "sku": self.sku_input.text().strip() or None,
        }

    # =========================================================
    # EDIT MODE
    # =========================================================

    def set_data(
        self,
        *,
        product_id,
        name: str,
        length: int,
        stock_quantity: int,
        reorder_level: int,
        cost_price: Decimal,
        selling_price: Decimal,
        sku: str | None,
    ) -> None:

        index = self.product_combo.findData(
            product_id
        )

        if index >= 0:
            self.product_combo.setCurrentIndex(
                index
            )

        self.name_input.setText(
            name
        )

        self.length_input.setValue(
            length
        )

        self.sku_input.setText(
            sku or ""
        )

        self.stock_quantity_input.setValue(
            stock_quantity
        )

        self.reorder_level_input.setValue(
            reorder_level
        )

        self.cost_price_input.setValue(
            float(cost_price)
        )

        self.selling_price_input.setValue(
            float(selling_price)
        )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self.name_input.clear()

        self.length_input.setValue(
            1
        )

        self.sku_input.clear()

        self.stock_quantity_input.setValue(
            0
        )

        self.reorder_level_input.setValue(
            5
        )

        self.cost_price_input.setValue(
            0.00
        )

        self.selling_price_input.setValue(
            0.00
        )

        self.product_combo.setCurrentIndex(
            -1
        )

        self.name_input.setFocus()

    # =========================================================
    # MODES
    # =========================================================

    def set_edit_mode(self) -> None:

        self.save_button.setText(
            "Update"
        )

    def set_create_mode(self) -> None:

        self.save_button.setText(
            "Save"
        )