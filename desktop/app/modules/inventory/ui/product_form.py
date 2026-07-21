from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.inventory.models.product import Product


from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
    QLineEdit,
)

from app.modules.inventory.models.category import Category


class ProductForm(QWidget):

    def __init__(self) -> None:
        super().__init__()
        self._selected_product: Product | None = None

        self.name_input = QLineEdit()
        self.brand_input = QLineEdit()
        self.category_combo = QComboBox()
        self.description_input = QTextEdit()
        self.save_button = QPushButton("Save")
        self.clear_button = QPushButton("Clear")

        form_layout = QFormLayout()
        form_layout.addRow(
            "Product Name:",
            self.name_input,
        )
        form_layout.addRow(
            "Brand:",
            self.brand_input,
        )
        form_layout.addRow(
            "Category:",
            self.category_combo,
        )
        form_layout.addRow(
            "Description:",
            self.description_input,
        )

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)

        layout = QVBoxLayout(self)
        layout.addLayout(form_layout)
        layout.addLayout(button_layout)

    def load_categories(
        self,
        categories: list[Category],
    ) -> None:
        self.category_combo.clear()

        for category in categories:
            self.category_combo.addItem(
                category.name,
                category.id,
            )

    def get_data(self) -> dict:
        return {
            "name": self.name_input.text(),
            "brand": self.brand_input.text(),
            "category_id": self.category_combo.currentData(),
            "description": self.description_input.toPlainText(),
        }
    
    def set_data(
        self,
        *,
        name: str,
        brand: str | None,
        category_id: int | None,
        description: str | None,
    ) -> None:

        self.name_input.setText(name)

        self.brand_input.setText(brand or "")

        self.description_input.setPlainText(
            description or ""
        )

        index = self.category_combo.findData(category_id)

        if index >= 0:
            self.category_combo.setCurrentIndex(index)

    def clear(self) -> None:
        self.clear_selection()
        self.name_input.clear()
        self.brand_input.clear()
        self.description_input.clear()
        self.category_combo.setCurrentIndex(-1)

    def selected_product(self) -> Product | None:
        return self._selected_product
    
    def set_selected_product(
        self,
        product: Product,
    ) -> None:

        self._selected_product = product

        self.set_data(
            name=product.name,
            brand=product.brand,
            category_id=product.category_id,
            description=product.description,
        )

    def clear_selection(self) -> None:
        self._selected_product = None   

    def product_name(self) -> str:
        return self.name_input.text()
    
    def brand(self) -> str:
        return self.brand_input.text()
    
    def description(self) -> str:
        return self.description_input.toPlainText()
    
    def category_id(self) -> int | None:
        return self.category_combo.currentData()
    
    def set_edit_mode(self) -> None:
        self.save_button.setText("Update")

    def set_create_mode(self) -> None:
        self.save_button.setText("Save")