from __future__ import annotations

from collections.abc import Callable
from uuid import UUID

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from app.core.ui.base_window import BaseWindow

from app.modules.inventory.exceptions import (
    InvalidProductNameError,
    ProductAlreadyExistsError,
    ProductHasVariantsError,
    ProductNotFoundError,
)

from app.modules.inventory.models.product import Product

from app.modules.inventory.services.category_service import (
    CategoryService,
)

from app.modules.inventory.services.product_service import (
    ProductService,
)

from app.modules.inventory.ui.product_form import (
    ProductForm,
)

from app.modules.inventory.ui.product_table import (
    ProductTable,
)


class ProductWindow(BaseWindow):

    def __init__(
        self,
        product_service: ProductService,
        category_service: CategoryService,
        refresh_product_variants: Callable[[], None],
    ) -> None:

        super().__init__()

        self._product_service = (
            product_service
        )

        self._category_service = (
            category_service
        )

        self._refresh_product_variants = (
            refresh_product_variants
        )

        self._selected_product_id: UUID | None = None

        self._build_ui()
        self._connect_signals()

        self.load_categories()
        self.load_products()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Product Management"
        )

        self.setObjectName(
            "productWindow"
        )

        self.resize(
            1100,
            650,
        )

        # =====================================================
        # FORM
        # =====================================================

        self.form = ProductForm()

        self.delete_button = QPushButton(
            "Delete"
        )

        self.delete_button.setObjectName(
            "productDeleteButton"
        )

        self.delete_button.setMinimumHeight(
            40
        )

        form_layout = QVBoxLayout()

        form_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        form_layout.setSpacing(
            8
        )

        form_layout.addWidget(
            self.form
        )

        form_layout.addWidget(
            self.delete_button
        )

        form_widget = QWidget()

        form_widget.setObjectName(
            "productFormContainer"
        )

        form_widget.setLayout(
            form_layout
        )

        # =====================================================
        # TABLE
        # =====================================================

        self.table = ProductTable()

        # =====================================================
        # SPLITTER
        # =====================================================

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.setObjectName(
            "productSplitter"
        )

        splitter.addWidget(
            form_widget
        )

        splitter.addWidget(
            self.table
        )

        splitter.setSizes(
            [
                350,
                750,
            ]
        )

        form_widget.setMinimumWidth(
            320
        )

        self.table.setMinimumWidth(
            500
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        main_layout = QVBoxLayout(
            self
        )

        main_layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        main_layout.addWidget(
            splitter
        )

    # =========================================================
    # SIGNALS
    # =========================================================

    def _connect_signals(self) -> None:

        self.form.save_button.clicked.connect(
            self.save
        )

        self.form.clear_button.clicked.connect(
            self.clear_form
        )

        self.delete_button.clicked.connect(
            self.delete
        )

        self.table.product_selected.connect(
            self.edit_selected
        )

    # =========================================================
    # CATEGORIES
    # =========================================================

    def load_categories(self) -> None:

        categories = (
            self._category_service.get_all()
        )

        self.form.load_categories(
            categories
        )

    # =========================================================
    # REFRESH CATEGORIES
    # =========================================================

    def refresh_categories(self) -> None:
        """
        Refresh the category list used by the
        product form.

        This is called when a category is
        created, updated, or deleted.
        """

        self.load_categories()

    # =========================================================
    # PRODUCTS
    # =========================================================

    def load_products(self) -> None:

        products = (
            self._product_service.get_all()
        )

        categories = (
            self._category_service.get_all()
        )

        category_names = {
            category.id: category.name
            for category in categories
            if category.id is not None
        }

        self.table.set_products(
            products,
            category_names,
        )

    # =========================================================
    # SAVE / UPDATE
    # =========================================================

    def save(self) -> None:

        data = self.form.get_data()

        try:

            if self._selected_product_id is None:

                self._product_service.create(
                    **data
                )

                # -------------------------------------------------
                # The product list has changed.
                #
                # Refresh ProductVariantWindow so the newly
                # created product immediately appears in its
                # product combo box.
                # -------------------------------------------------

                self._refresh_product_variants()

                self.show_information(
                    "Product created successfully."
                )

            else:

                self._product_service.update(
                    self._selected_product_id,
                    **data,
                )

                self.show_information(
                    "Product updated successfully."
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

    # =========================================================
    # EDIT
    # =========================================================

    def edit_selected(
        self,
        product: Product,
    ) -> None:

        if product.id is None:
            return

        self._selected_product_id = (
            product.id
        )

        self.form.set_selected_product(
            product
        )

        self.form.set_edit_mode()

    # =========================================================
    # DELETE
    # =========================================================

    def delete(self) -> None:

        product = (
            self.table.selected_product()
        )

        if product is None:
            return

        if product.id is None:
            return

        if not self.ask_confirmation(
            "Delete Product",
            f'Delete "{product.name}"?',
        ):
            return

        try:

            self._product_service.delete(
                product.id
            )

            self.clear_form()
            self.load_products()

        except ProductHasVariantsError as error:

            self.show_error(
                str(error)
            )

        except ProductNotFoundError as error:

            self.show_error(
                str(error)
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_form(self) -> None:

        self._selected_product_id = None

        self.form.clear()

        self.form.set_create_mode()