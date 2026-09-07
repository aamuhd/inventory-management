from __future__ import annotations

from uuid import UUID

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class RoleForm(QWidget):

    def __init__(self) -> None:

        super().__init__()

        self.setObjectName(
            "roleForm"
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        title = QLabel(
            "Role Information"
        )

        title.setObjectName(
            "roleFormTitle"
        )

        # -----------------------------------------------------
        # Name
        # -----------------------------------------------------

        self.name_input = QLineEdit()

        self.name_input.setObjectName(
            "roleNameInput"
        )

        self.name_input.setPlaceholderText(
            "Enter role name"
        )

        # -----------------------------------------------------
        # Description
        # -----------------------------------------------------

        self.description_input = QTextEdit()

        self.description_input.setObjectName(
            "roleDescriptionInput"
        )

        self.description_input.setPlaceholderText(
            "Enter role description"
        )

        self.description_input.setMaximumHeight(
            120
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

        form_layout.setVerticalSpacing(
            12
        )

        form_layout.addRow(
            "Name:",
            self.name_input,
        )

        form_layout.addRow(
            "Description:",
            self.description_input,
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.setObjectName(
            "roleSaveButton"
        )

        self.clear_button = QPushButton(
            "Clear"
        )

        self.clear_button.setObjectName(
            "roleClearButton"
        )

        for button in (
            self.save_button,
            self.clear_button,
        ):
            button.setMinimumHeight(
                38
            )

            button.setCursor(
                Qt.CursorShape.PointingHandCursor
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

        # -----------------------------------------------------
        # Main Layout
        # -----------------------------------------------------

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            15,
            15,
            15,
            15,
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

        layout.addStretch()

        layout.addLayout(
            button_layout
        )

    # =========================================================
    # DATA
    # =========================================================

    def get_data(self) -> dict:

        return {
            "name": (
                self.name_input
                .text()
                .strip()
            ),
            "description": (
                self.description_input
                .toPlainText()
                .strip()
                or None
            ),
        }

    # =========================================================
    # EDIT
    # =========================================================

    def set_data(
        self,
        *,
        name: str,
        description: str | None,
    ) -> None:

        self.name_input.setText(
            name
        )

        self.description_input.setPlainText(
            description or ""
        )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self.name_input.clear()

        self.description_input.clear()

        self.name_input.setFocus()

    # =========================================================
    # MODES
    # =========================================================

    def set_create_mode(self) -> None:

        self.save_button.setText(
            "Save"
        )

    def set_edit_mode(self) -> None:

        self.save_button.setText(
            "Update"
        )