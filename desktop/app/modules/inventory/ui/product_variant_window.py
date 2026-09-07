from __future__ import annotations

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
    ProductVariantAlreadyExistsError,
    ProductVariantNotFoundError,
)

from app.modules.inventory.services.product_service import (
    ProductService,
)

from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)

from app.modules.inventory.ui.product_variant_form import (
    ProductVariantForm,
)

from app.modules.inventory.ui.product_variant_table import (
    ProductVariantTable,
)


class ProductVariantWindow(BaseWindow):

    def __init__(
        self,
        variant_service: ProductVariantService,
        product_service: ProductService,
    ) -> None:

        super().__init__()

        self._variant_service = variant_service
        self._product_service = product_service

        self._selected_variant_id: UUID | None = None

        self._build_ui()
        self._connect_signals()

        self.load_products()
        self.load_variants()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Product Variant Management"
        )

        self.setObjectName(
            "productVariantWindow"
        )

        self.resize(
            1100,
            650,
        )

        self.setMinimumSize(
            850,
            500,
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        self.form = ProductVariantForm()

        form_container = QVBoxLayout()

        form_container.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        form_container.addWidget(
            self.form
        )

        self.delete_button = QPushButton(
            "Delete"
        )

        self.delete_button.setObjectName(
            "productVariantDeleteButton"
        )

        self.delete_button.setMinimumHeight(
            40
        )

        self.delete_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        form_container.addWidget(
            self.delete_button
        )

        form_widget = QWidget()

        form_widget.setObjectName(
            "productVariantFormContainer"
        )

        form_widget.setLayout(
            form_container
        )

        form_widget.setMinimumWidth(
            320
        )

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        self.table = ProductVariantTable()

        self.table.setObjectName(
            "productVariantTableContainer"
        )

        self.table.setMinimumWidth(
            500
        )

        # -----------------------------------------------------
        # Splitter
        # -----------------------------------------------------

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.setObjectName(
            "productVariantSplitter"
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

        # -----------------------------------------------------
        # Main Layout
        # -----------------------------------------------------

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

        self.table.variant_selected.connect(
            self.edit_selected
        )

    # =========================================================
    # PRODUCTS
    # =========================================================

    def load_products(self) -> None:

        products = (
            self._product_service.get_all()
        )

        self.form.load_products(
            products
        )

    # =========================================================
    # VARIANTS
    # =========================================================

    def load_variants(self) -> None:

        variants = (
            self._variant_service.get_all()
        )

        products = (
            self._product_service.get_all()
        )

        product_names = {
            product.id: product.name
            for product in products
            if product.id is not None
        }

        self.table.set_variants(
            variants,
            product_names,
        )

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh(self) -> None:
        """
        Refresh the Product Variant window after the product
        list changes.

        Both the product combo box and the variant table need
        to be refreshed because a newly created product must
        become available when adding a variant.
        """

        self.load_products()
        self.load_variants()

    # =========================================================
    # SAVE / UPDATE
    # =========================================================

    def save(self) -> None:

        data = self.form.get_data()

        try:

            if self._selected_variant_id is None:

                self._variant_service.create(
                    **data
                )

                self.show_information(
                    "Product variant created successfully."
                )

            else:

                self._variant_service.update(
                    self._selected_variant_id,
                    **data,
                )

                self.show_information(
                    "Product variant updated successfully."
                )

            self.clear_form()
            self.load_variants()

        except (
            ProductVariantAlreadyExistsError,
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
        variant,
    ) -> None:

        if variant.id is None:
            return

        self._selected_variant_id = (
            variant.id
        )

        self.form.set_data(
            product_id=variant.product_id,
            name=variant.name,
            length=variant.length,
            stock_quantity=variant.stock_quantity,
            reorder_level=variant.reorder_level,
            cost_price=variant.cost_price,
            selling_price=variant.selling_price,
            sku=variant.sku,
        )

        self.form.set_edit_mode()

    # =========================================================
    # DELETE
    # =========================================================

    def delete(self) -> None:

        variant = (
            self.table.selected_variant()
        )

        if variant is None:
            return

        if variant.id is None:
            return

        if not self.ask_confirmation(
            "Delete Product Variant",
            f'Delete "{variant.name}"?',
        ):
            return

        try:

            self._variant_service.delete(
                variant.id
            )

            self.clear_form()
            self.load_variants()

        except ProductVariantNotFoundError as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_form(self) -> None:

        self._selected_variant_id = None

        self.form.clear()

        self.form.set_create_mode()
