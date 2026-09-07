from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class CategoryForm(QWidget):
    """
    Form used for creating and updating categories.

    This widget is responsible only for collecting user input.
    It does not communicate with the database or services.
    """

    def __init__(self) -> None:
        super().__init__()

        self.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred,
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setObjectName("categoryForm")

        title = QLabel("Category Information")
        title.setObjectName("formSectionTitle")

        title.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Fixed,
        )

        # -----------------------------------------------------
        # Inputs
        # -----------------------------------------------------

        self.name_input = QLineEdit()
        self.name_input.setObjectName("formLineEdit")

        self.name_input.setPlaceholderText(
            "Enter category name"
        )

        self.name_input.setMinimumHeight(35)

        self.description_input = QTextEdit()
        self.description_input.setObjectName("formTextEdit")

        self.description_input.setPlaceholderText(
            "Enter category description"
        )

        self.description_input.setMinimumHeight(
            100
        )

        self.description_input.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
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

        form_layout.addRow(
            "Category Name:",
            self.name_input,
        )

        form_layout.addRow(
            "Description:",
            self.description_input,
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.save_button = QPushButton("Save")
        self.save_button.setObjectName("primaryButton")

        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("secondaryButton")

        self.save_button.setMinimumHeight(
            35
        )

        self.clear_button.setMinimumHeight(
            35
        )

        button_layout = QHBoxLayout()

        button_layout.addStretch()

        button_layout.addWidget(
            self.save_button
        )

        button_layout.addWidget(
            self.clear_button
        )

        # -----------------------------------------------------
        # Main layout
        # -----------------------------------------------------

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            10,
            10,
            10,
            10,
        )

        main_layout.setSpacing(10)

        main_layout.addWidget(
            title
        )

        main_layout.addLayout(
            form_layout
        )

        main_layout.addLayout(
            button_layout
        )

        # Give the description field the available
        # vertical space.
        main_layout.setStretch(
            1,
            1,
        )

    # =========================================================
    # DATA
    # =========================================================

    def category_data(
        self,
    ) -> tuple[str, str]:

        return (
            self.name_input.text(),
            self.description_input.toPlainText(),
        )

    # =========================================================
    # EDIT MODE
    # =========================================================

    def set_category(
        self,
        name: str,
        description: str,
    ) -> None:

        self.name_input.setText(
            name
        )

        self.description_input.setPlainText(
            description
        )

    def set_edit_mode(
        self,
    ) -> None:

        self.save_button.setText(
            "Update"
        )

    def set_create_mode(
        self,
    ) -> None:

        self.save_button.setText(
            "Save"
        )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self.name_input.clear()

        self.description_input.clear()

        self.name_input.setFocus()