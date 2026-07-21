from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.exceptions import (
    InvalidProductNameError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
)
from app.modules.inventory.models.product import Product
from app.modules.inventory.services.category_service import CategoryService
from app.modules.inventory.services.product_service import ProductService
from app.modules.inventory.ui.product_form import ProductForm
from app.modules.inventory.ui.product_table import ProductTable


class ProductWindow(QWidget):

    def __init__(
        self,
        product_service: ProductService,
        category_service: CategoryService,
    ) -> None:
        super().__init__()

        self._product_service = product_service
        self._category_service = category_service

        self._selected_product_id = None

        self._build_ui()
        self._connect_signals()

        self.load_categories()
        self.load_products()

    def _build_ui(self) -> None:

        self.setWindowTitle("Product Management")

        self.form = ProductForm()

        self.table = ProductTable()

        self.delete_button = QPushButton("Delete")

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.form)
        left_layout.addWidget(self.delete_button)

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(self.table, 2)

    def _connect_signals(self) -> None:

        self.form.save_button.clicked.connect(self.save)

        self.form.clear_button.clicked.connect(
            self.clear_form
        )

        self.delete_button.clicked.connect(
            self.delete
        )

        self.table.product_selected.connect(
            self.edit_selected
        )

    def load_categories(self) -> None:

        categories = self._category_service.get_all()

        self.form.load_categories(categories)

    def load_products(self) -> None:

        products = self._product_service.get_all()

        categories = self._category_service.get_all()

        category_names = {
            category.id: category.name
            for category in categories
            if category.id is not None
        }

        self.table.set_products(
            products,
            category_names,
        )

    def save(self) -> None:

        data = self.form.get_data()

        try:

            if self._selected_product_id is None:

                self._product_service.create(**data)

                QMessageBox.information(
                    self,
                    "Success",
                    "Product created successfully.",
                )

            else:

                self._product_service.update(
                    self._selected_product_id,
                    **data,
                )

                QMessageBox.information(
                    self,
                    "Success",
                    "Product updated successfully.",
                )

            self.clear_form()

            self.load_products()

        except (
            ProductAlreadyExistsError,
            InvalidProductNameError,
        ) as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    def edit_selected(
        self,
        product: Product,
    ) -> None:

        self._selected_product_id = product.id

        self.form.set_data(
            name=product.name,
            brand=product.brand,
            category_id=product.category_id,
            description=product.description,
        )

        self.form.set_edit_mode()

    def delete(self) -> None:

        product = self.table.selected_product()

        if product is None:
            return

        answer = QMessageBox.question(
            self,
            "Delete Product",
            f'Delete "{product.name}"?',
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:

            self._product_service.delete(product.id)

            self.clear_form()

            self.load_products()

        except ProductNotFoundError as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    def clear_form(self) -> None:

        self._selected_product_id = None
        self.form.clear()
        self.form.set_create_mode()