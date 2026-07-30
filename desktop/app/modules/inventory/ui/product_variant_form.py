from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.inventory.models.product_variant import ProductVariant
    from app.modules.inventory.models.product import Product

from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class ProductVariantForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self._selected_variant: ProductVariant | None = None

        self.product_combo = QComboBox()

        self.length_spin = QSpinBox()
        self.length_spin.setMinimum(1)

        self.stock_quantity_spin = QSpinBox()
        self.stock_quantity_spin.setMinimum(0)

        self.reorder_level_spin = QSpinBox()
        self.reorder_level_spin.setMinimum(0)

        self.cost_price_spin = QDoubleSpinBox()
        self.cost_price_spin.setMinimum(0)
        self.cost_price_spin.setMaximum(1_000_000)
        self.cost_price_spin.setDecimals(2)

        self.selling_price_spin = QDoubleSpinBox()
        self.selling_price_spin.setMinimum(0)
        self.selling_price_spin.setMaximum(1_000_000)
        self.selling_price_spin.setDecimals(2)

        self.barcode_input = QLineEdit()

        self.sku_input = QLineEdit()

        self.save_button = QPushButton("Save")
        self.clear_button = QPushButton("Clear")

        form_layout = QFormLayout()

        form_layout.addRow(
            "Product:",
            self.product_combo,
        )

        form_layout.addRow(
            "Length:",
            self.length_spin,
        )

        form_layout.addRow(
            "Stock Quantity:",
            self.stock_quantity_spin,
        )

        form_layout.addRow(
            "Reorder Level:",
            self.reorder_level_spin,
        )

        form_layout.addRow(
            "Cost Price:",
            self.cost_price_spin,
        )

        form_layout.addRow(
            "Selling Price:",
            self.selling_price_spin,
        )

        form_layout.addRow(
            "Barcode:",
            self.barcode_input,
        )

        form_layout.addRow(
            "SKU:",
            self.sku_input,
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)

        layout = QVBoxLayout(self)

        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

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

    def get_data(self) -> dict:

        return {
            "product_id": self.product_combo.currentData(),
            "length": self.length_spin.value(),
            "stock_quantity": self.stock_quantity_spin.value(),
            "reorder_level": self.reorder_level_spin.value(),
            "cost_price": Decimal(
                str(
                    self.cost_price_spin.value(),
                )
            ),
            "selling_price": Decimal(
                str(
                    self.selling_price_spin.value(),
                )
            ),
            "barcode": self.barcode_input.text() or None,
            "sku": self.sku_input.text() or None,
        }

    def set_data(
        self,
        *,
        product_id,
        length: int,
        stock_quantity: int,
        reorder_level: int,
        cost_price: Decimal,
        selling_price: Decimal,
        barcode: str | None,
        sku: str | None,
    ) -> None:

        index = self.product_combo.findData(product_id)

        if index >= 0:
            self.product_combo.setCurrentIndex(index)

        self.length_spin.setValue(length)

        self.stock_quantity_spin.setValue(stock_quantity)

        self.reorder_level_spin.setValue(reorder_level)

        self.cost_price_spin.setValue(
            float(cost_price)
        )

        self.selling_price_spin.setValue(
            float(selling_price)
        )

        self.barcode_input.setText(
            barcode or "",
        )

        self.sku_input.setText(
            sku or "",
        )

    def clear(self) -> None:

        self.clear_selection()

        self.product_combo.setCurrentIndex(-1)

        self.length_spin.setValue(1)

        self.stock_quantity_spin.setValue(0)

        self.reorder_level_spin.setValue(0)

        self.cost_price_spin.setValue(0)

        self.selling_price_spin.setValue(0)

        self.barcode_input.clear()

        self.sku_input.clear()

    def selected_variant(
        self,
    ) -> ProductVariant | None:

        return self._selected_variant

    def set_selected_variant(
        self,
        variant: ProductVariant,
    ) -> None:

        self._selected_variant = variant

        self.set_data(
            product_id=variant.product_id,
            length=variant.length,
            stock_quantity=variant.stock_quantity,
            reorder_level=variant.reorder_level,
            cost_price=variant.cost_price,
            selling_price=variant.selling_price,
            barcode=variant.barcode,
            sku=variant.sku,
        )

    def clear_selection(self) -> None:

        self._selected_variant = None

    def set_edit_mode(self) -> None:

        self.save_button.setText("Update")

    def set_create_mode(self) -> None:

        self.save_button.setText("Save")