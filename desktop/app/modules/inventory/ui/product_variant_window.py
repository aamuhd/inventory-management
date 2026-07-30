from PySide6.QtWidgets import (
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)

from app.core.ui.base_window import BaseWindow
from app.modules.inventory.exceptions import (
    InvalidLengthError,
    InvalidPriceError,
    InvalidStockQuantityError,
    ProductVariantAlreadyExistsError,
    ProductVariantNotFoundError,
)
from app.modules.inventory.models.product_variant import ProductVariant
from app.modules.inventory.services.product_service import ProductService
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

        self._selected_variant_id = None

        self._build_ui()
        self._connect_signals()

        self.load_products()
        self.load_variants()

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Product Variant Management",
        )

        self.form = ProductVariantForm()

        self.table = ProductVariantTable()

        self.delete_button = QPushButton(
            "Delete",
        )

        left_layout = QVBoxLayout()

        left_layout.addWidget(
            self.form,
        )

        left_layout.addWidget(
            self.delete_button,
        )

        main_layout = QHBoxLayout(self)

        main_layout.addLayout(
            left_layout,
            1,
        )

        main_layout.addWidget(
            self.table,
            2,
        )

    def _connect_signals(self) -> None:

        self.form.save_button.clicked.connect(
            self.save,
        )

        self.form.clear_button.clicked.connect(
            self.clear_form,
        )

        self.delete_button.clicked.connect(
            self.delete,
        )

        self.table.variant_selected.connect(
            self.edit_selected,
        )

    def load_products(self) -> None:

        products = self._product_service.get_all()

        self.form.load_products(
            products,
        )

    def load_variants(self) -> None:

        variants = self._variant_service.get_all()

        self.table.set_variants(
            variants,
        )

    def save(self) -> None:

        data = self.form.get_data()

        try:

            if self._selected_variant_id is None:

                self._variant_service.create(
                    **data,
                )

                self.show_information(
                    "Product variant created successfully.",
                )

            else:

                self._variant_service.update(
                    self._selected_variant_id,
                    **data,
                )

                self.show_information(
                    "Product variant updated successfully.",
                )

            self.clear_form()

            self.load_variants()

        except (
            ProductVariantAlreadyExistsError,
            InvalidLengthError,
            InvalidStockQuantityError,
            InvalidPriceError,
        ) as error:

            self.show_error(
                str(error),
            )

    def edit_selected(
        self,
        variant: ProductVariant,
    ) -> None:

        self._selected_variant_id = variant.id

        self.form.set_selected_variant(
            variant,
        )

        self.form.set_edit_mode()

    def delete(self) -> None:

        variant = self.table.selected_variant()

        if variant is None:
            return

        if not self.ask_confirmation(
            "Delete Product Variant",
            (
                f"Delete variant "
                f"{variant.product.name} - "
                f"{variant.length}?"
            ),
        ):
            return

        try:

            self._variant_service.delete(
                variant.id,
            )

            self.clear_form()

            self.load_variants()

            self.show_information(
                "Product variant deleted successfully.",
            )

        except ProductVariantNotFoundError as error:

            self.show_error(
                str(error),
            )

    def clear_form(self) -> None:

        self._selected_variant_id = None

        self.form.clear()

        self.form.set_create_mode()

        self.table.clear_selection()