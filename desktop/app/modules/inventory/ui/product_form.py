from __future__ import annotations

from typing import TYPE_CHECKING

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.models.category import Category

if TYPE_CHECKING:
    from app.modules.inventory.models.product import Product


class ProductForm(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self._selected_product: Product | None = None

        self.setObjectName(
            "productForm"
        )

        self._build_ui()

    def _build_ui(self) -> None:

        # =====================================================
        # TITLE
        # =====================================================

        title = QLabel(
            "Product Information"
        )

        title.setObjectName(
            "productFormTitle"
        )

        # =====================================================
        # INPUTS
        # =====================================================

        self.name_input = QLineEdit()

        self.name_input.setObjectName(
            "productNameInput"
        )

        self.name_input.setPlaceholderText(
            "Enter product name"
        )

        self.brand_input = QLineEdit()

        self.brand_input.setObjectName(
            "productBrandInput"
        )

        self.brand_input.setPlaceholderText(
            "Enter brand"
        )

        self.category_combo = QComboBox()

        self.category_combo.setObjectName(
            "productCategoryCombo"
        )

        self.category_combo.setMinimumHeight(
            35
        )

        self.description_input = QTextEdit()

        self.description_input.setObjectName(
            "productDescriptionInput"
        )

        self.description_input.setPlaceholderText(
            "Enter product description"
        )

        self.description_input.setMinimumHeight(
            120
        )

        # =====================================================
        # FORM
        # =====================================================

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

        # =====================================================
        # BUTTONS
        # =====================================================

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.setObjectName(
            "productSaveButton"
        )

        self.clear_button = QPushButton(
            "Clear"
        )

        self.clear_button.setObjectName(
            "productClearButton"
        )

        self.save_button.setMinimumHeight(
            38
        )

        self.clear_button.setMinimumHeight(
            38
        )

        button_layout = QHBoxLayout()

        button_layout.setSpacing(
            8
        )

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            10,
            10,
            10,
            10,
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

        layout.addLayout(
            button_layout
        )

        layout.addStretch()

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
            "name": self.name_input.text().strip(),
            "brand": self.brand_input.text().strip(),
            "category_id": self.category_combo.currentData(),
            "description": (
                self.description_input
                .toPlainText()
                .strip()
            ),
        }

    def set_data(
        self,
        *,
        name: str,
        brand: str | None,
        category_id: int | None,
        description: str | None,
    ) -> None:

        self.name_input.setText(
            name
        )

        self.brand_input.setText(
            brand or ""
        )

        self.description_input.setPlainText(
            description or ""
        )

        index = self.category_combo.findData(
            category_id
        )

        if index >= 0:
            self.category_combo.setCurrentIndex(
                index
            )

    def clear(self) -> None:

        self.clear_selection()

        self.name_input.clear()
        self.brand_input.clear()
        self.description_input.clear()

        self.category_combo.setCurrentIndex(
            -1
        )

        self.name_input.setFocus()

    def selected_product(
        self,
    ) -> Product | None:

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

    def set_edit_mode(self) -> None:

        self.save_button.setText(
            "Update"
        )

    def set_create_mode(self) -> None:

        self.save_button.setText(
            "Save"
        )