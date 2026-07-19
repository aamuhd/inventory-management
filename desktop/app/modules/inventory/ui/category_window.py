from PySide6.QtWidgets import (
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from app.modules.inventory.exceptions import (
    CategoryAlreadyExistsError,
    CategoryNotFoundError,
    InvalidCategoryNameError,
)
from app.modules.inventory.models.category import Category
from app.modules.inventory.services.category_service import CategoryService
from app.modules.inventory.ui.category_form import CategoryForm
from app.modules.inventory.ui.category_table import CategoryTable


class CategoryWindow(QWidget):

    def __init__(
        self,
        category_service: CategoryService,
    ) -> None:
        super().__init__()

        self._category_service = category_service
        self._selected_category_id: int | None = None

        #self._selected_category: Category | None = None

        self._build_ui()
        self._connect_signals()

        self.load_categories()

    def _build_ui(self) -> None:

        self.setWindowTitle("Category Management")

        self.form = CategoryForm()

        self.table = CategoryTable()

        self.delete_button = QPushButton("Delete")

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.form)
        left_layout.addWidget(self.delete_button)

        main_layout = QHBoxLayout(self)
        main_layout.addLayout(left_layout, 1)
        main_layout.addWidget(self.table, 2)

    def _connect_signals(self) -> None:

        self.form.save_button.clicked.connect(self.save)

        self.form.clear_button.clicked.connect(self.clear_form)

        self.delete_button.clicked.connect(self.delete)

        self.table.category_selected.connect(
            self.edit_selected
        )

    def load_categories(self) -> None:

        categories = self._category_service.get_all()

        self.table.set_categories(categories)

    def save(self) -> None:

        name, description = self.form.category_data()

        try:
            if self._selected_category_id is None:

                self._category_service.create(
                    name,
                    description,
                )

                QMessageBox.information(
                    self,
                    "Success",
                    "Category created successfully.",
                )

            else:

                self._category_service.update(
                    self._selected_category_id,
                    name,
                    description,
                )

                QMessageBox.information(
                    self,
                    "Success",
                    "Category updated successfully.",
                )

            self.clear_form()
            self.load_categories()

        except (
            CategoryAlreadyExistsError,
            InvalidCategoryNameError,
        ) as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )
        
    def edit_selected(self, category: Category) -> None:
        if category.id is None:
            return

        self._selected_category_id = category.id

        self.form.set_category(
            category.name,
            category.description,
        )
        self.form.set_edit_mode()

    def delete(self) -> None:

        category = self.table.selected_category()

        if category is None or category.id is None:
            return

        answer = QMessageBox.question(
            self,
            "Delete Category",
            f'Delete "{category.name}"?',
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        try:
            self._category_service.delete(category.id)

            self.clear_form()
            self.load_categories()

        except CategoryNotFoundError as error:

            QMessageBox.warning(
                self,
                "Error",
                str(error),
            )

    def clear_form(self) -> None:
        self._selected_category_id = None
        self.form.clear()
        self.form.set_create_mode()