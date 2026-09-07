from __future__ import annotations

from collections.abc import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMessageBox,
    QSplitter,
    QVBoxLayout,
    QWidget,
    QPushButton,
)

from app.core.ui.base_window import BaseWindow

from app.modules.inventory.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    InvalidCategoryNameError,
)

from app.modules.inventory.models.category import Category

from app.modules.inventory.services.category_service import (
    CategoryService,
)

from app.modules.inventory.ui.category_form import (
    CategoryForm,
)

from app.modules.inventory.ui.category_table import (
    CategoryTable,
)


class CategoryWindow(BaseWindow):

    def __init__(
        self,
        category_service: CategoryService,
        refresh_products: Callable[[], None],
    ) -> None:

        super().__init__()

        self._category_service = category_service

        self._refresh_products = (
            refresh_products
        )

        self._selected_category_id: int | None = None

        self._build_ui()
        self._connect_signals()

        self.load_categories()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Category Management"
        )

        self.setObjectName(
            "categoryWindow"
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        self.form = CategoryForm()

        self.delete_button = QPushButton(
            "Delete"
        )

        self.delete_button.setMinimumHeight(
            40
        )

        form_widget = QWidget()

        form_widget.setObjectName(
            "categoryFormContainer"
        )

        form_layout = QVBoxLayout(
            form_widget
        )

        form_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        form_layout.addWidget(
            self.form
        )

        form_layout.addWidget(
            self.delete_button
        )

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        self.table = CategoryTable()

        # -----------------------------------------------------
        # Splitter
        # -----------------------------------------------------

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.setObjectName(
            "categorySplitter"
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

        # Form should not become too small.
        form_widget.setMinimumWidth(
            300
        )

        # Table should not become too small.
        self.table.setMinimumWidth(
            400
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

    def _connect_signals(
        self,
    ) -> None:

        self.form.save_button.clicked.connect(
            self.save
        )

        self.form.clear_button.clicked.connect(
            self.clear_form
        )

        self.delete_button.clicked.connect(
            self.delete
        )

        self.table.category_selected.connect(
            self.edit_selected
        )

    # =========================================================
    # LOAD
    # =========================================================

    def load_categories(
        self,
    ) -> None:

        categories = (
            self._category_service.get_all()
        )

        self.table.set_categories(
            categories
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save(
        self,
    ) -> None:

        name, description = (
            self.form.category_data()
        )

        try:

            if (
                self._selected_category_id
                is None
            ):

                self._category_service.create(
                    name,
                    description,
                )

                self.show_information(
                    "Category created successfully.",
                )

            else:

                self._category_service.update(
                    self._selected_category_id,
                    name,
                    description,
                )

                self.show_information(
                    "Category updated successfully.",
                )

            self.clear_form()

            self.load_categories()

            # -------------------------------------------------
            # Refresh Product Window
            # -------------------------------------------------

            self._refresh_products()

        except (
            CategoryAlreadyExistsError,
            InvalidCategoryNameError,
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
        category: Category,
    ) -> None:

        if category.id is None:
            return

        self._selected_category_id = (
            category.id
        )

        self.form.set_category(
            category.name,
            category.description,
        )

        self.form.set_edit_mode()

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
    ) -> None:

        category = (
            self.table.selected_category()
        )

        if (
            category is None
            or category.id is None
        ):
            return

        if not self.ask_confirmation(
            "Delete Category",
            (
                f"Are you sure you want to "
                f"delete {category.name}?"
            ),
        ):
            return

        try:

            self._category_service.delete(
                category.id
            )

            self.clear_form()

            self.load_categories()

            # -------------------------------------------------
            # Refresh Product Window
            # -------------------------------------------------

            self._refresh_products()

        except CategoryNotFoundError as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_form(
        self,
    ) -> None:

        self._selected_category_id = None

        self.form.clear()

        self.form.set_create_mode()