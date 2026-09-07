from __future__ import annotations

from uuid import UUID

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class UserForm(QWidget):

    def __init__(self) -> None:

        super().__init__()

        self.setObjectName(
            "userForm"
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        title = QLabel(
            "User Information"
        )

        title.setObjectName(
            "userFormTitle"
        )

        # -----------------------------------------------------
        # Username
        # -----------------------------------------------------

        self.username_input = QLineEdit()

        self.username_input.setObjectName(
            "userUsernameInput"
        )

        self.username_input.setPlaceholderText(
            "Enter username"
        )

        # -----------------------------------------------------
        # Full Name
        # -----------------------------------------------------

        self.full_name_input = QLineEdit()

        self.full_name_input.setObjectName(
            "userFullNameInput"
        )

        self.full_name_input.setPlaceholderText(
            "Enter full name"
        )

        # -----------------------------------------------------
        # Email
        # -----------------------------------------------------

        self.email_input = QLineEdit()

        self.email_input.setObjectName(
            "userEmailInput"
        )

        self.email_input.setPlaceholderText(
            "Enter email"
        )

        # -----------------------------------------------------
        # Password
        # -----------------------------------------------------

        self.password_input = QLineEdit()

        self.password_input.setObjectName(
            "userPasswordInput"
        )

        self.password_input.setPlaceholderText(
            "Enter password"
        )

        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        # -----------------------------------------------------
        # Role
        # -----------------------------------------------------

        self.role_combo = QComboBox()

        self.role_combo.setObjectName(
            "userRoleCombo"
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
            "Username:",
            self.username_input,
        )

        form_layout.addRow(
            "Full Name:",
            self.full_name_input,
        )

        form_layout.addRow(
            "Email:",
            self.email_input,
        )

        form_layout.addRow(
            "Password:",
            self.password_input,
        )

        form_layout.addRow(
            "Role:",
            self.role_combo,
        )

        # -----------------------------------------------------
        # Buttons
        # -----------------------------------------------------

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.setObjectName(
            "userSaveButton"
        )

        self.clear_button = QPushButton(
            "Clear"
        )

        self.clear_button.setObjectName(
            "userClearButton"
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
    # ROLES
    # =========================================================

    def load_roles(
        self,
        roles,
    ) -> None:

        self.role_combo.clear()

        for role in roles:

            self.role_combo.addItem(
                role.name,
                role.id,
            )

    # =========================================================
    # DATA
    # =========================================================

    def get_data(self) -> dict:

        return {
            "username": (
                self.username_input
                .text()
                .strip()
            ),
            "full_name": (
                self.full_name_input
                .text()
                .strip()
            ),
            "email": (
                self.email_input
                .text()
                .strip()
                or None
            ),
            "password": (
                self.password_input
                .text()
            ),
            "role_id": (
                self.role_combo.currentData()
            ),
        }

    # =========================================================
    # EDIT
    # =========================================================

    def set_data(
        self,
        *,
        username: str,
        full_name: str,
        email: str | None,
        role_id: UUID,
    ) -> None:

        self.username_input.setText(
            username
        )

        self.full_name_input.setText(
            full_name
        )

        self.email_input.setText(
            email or ""
        )

        self.password_input.clear()

        index = self.role_combo.findData(
            role_id
        )

        if index >= 0:
            self.role_combo.setCurrentIndex(
                index
            )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self.username_input.clear()
        self.full_name_input.clear()
        self.email_input.clear()
        self.password_input.clear()

        self.role_combo.setCurrentIndex(
            -1
        )

        self.username_input.setFocus()

    # =========================================================
    # MODES
    # =========================================================

    def set_create_mode(self) -> None:

        self.save_button.setText(
            "Save"
        )

        self.password_input.setPlaceholderText(
            "Enter password"
        )

    def set_edit_mode(self) -> None:

        self.save_button.setText(
            "Update"
        )

        self.password_input.setPlaceholderText(
            "Leave blank to keep current password"
        )