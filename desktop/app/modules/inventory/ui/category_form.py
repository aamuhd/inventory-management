from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QFormLayout,
    QHBoxLayout,
    QVBoxLayout,
)


class CategoryForm(QWidget):
    """
    Form used for creating and updating categories.

    This widget is responsible only for collecting user input.
    It does not communicate with the database or services.
    """

    def __init__(self) -> None:
        super().__init__()

        self._build_ui()

    def _build_ui(self) -> None:
        title = QLabel("Category Information")

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter category name")

        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText(
            "Enter category description"
        )
        self.description_input.setFixedHeight(100)

        form_layout = QFormLayout()
        form_layout.addRow("Category Name:", self.name_input)
        form_layout.addRow("Description:", self.description_input)

        self.save_button = QPushButton("Save")

        self.clear_button = QPushButton("Clear")
        #self.cancel_button = QPushButton("Cancel")

        
        self.clear_button.clicked.connect(self.clear)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(title)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

    def category_data(self) -> tuple[str, str]:
        """
        Returns the values entered by the user.
        """
        return (
            self.name_input.text(),
            self.description_input.toPlainText(),
        )

    def set_category(
        self,
        name: str,
        description: str,
    ) -> None:
        """
        Populate the form when editing a category.
        """
        self.name_input.setText(name)
        self.description_input.setPlainText(description)

    def clear(self) -> None:
        """
        Clears the form.
        """
        self.name_input.clear()
        self.description_input.clear()

        self.name_input.setFocus()

    def set_edit_mode(self) -> None:
        self.save_button.setText("Update")

    def set_create_mode(self) -> None:
        self.save_button.setText("Save")