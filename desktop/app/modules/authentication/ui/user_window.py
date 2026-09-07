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

from app.modules.authentication.exceptions import (
    InvalidEmailError,
    InvalidFullNameError,
    InvalidPasswordError,
    InvalidUsernameError,
    RoleNotFoundError,
    UserAlreadyExistsError,
    UserNotFoundError,
)

from app.modules.authentication.models.user import User

from app.modules.authentication.repositories.role_repository import (
    RoleRepository,
)

from app.modules.authentication.services.user_service import (
    UserService,
)

from app.modules.authentication.ui.user_form import (
    UserForm,
)

from app.modules.authentication.ui.user_table import (
    UserTable,
)


class UserWindow(BaseWindow):

    def __init__(
        self,
        user_service: UserService,
        role_repository: RoleRepository,
    ) -> None:

        super().__init__()

        self._user_service = user_service
        self._role_repository = role_repository

        self._selected_user_id: UUID | None = None

        self._build_ui()
        self._connect_signals()

        self.load_roles()
        self.load_users()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "User Management"
        )

        self.setObjectName(
            "userWindow"
        )

        self.setMinimumSize(
            950,
            550,
        )

        self.resize(
            1200,
            700,
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        self.form = UserForm()

        self.delete_button = QPushButton(
            "Deactivate"
        )

        self.delete_button.setObjectName(
            "userDeactivateButton"
        )

        self.delete_button.setMinimumHeight(
            40
        )

        self.delete_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        form_layout = QVBoxLayout()

        form_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        form_layout.setSpacing(
            10
        )

        form_layout.addWidget(
            self.form
        )

        form_layout.addWidget(
            self.delete_button
        )

        form_widget = QWidget()

        form_widget.setObjectName(
            "userFormContainer"
        )

        form_widget.setLayout(
            form_layout
        )

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        self.table = UserTable()

        # -----------------------------------------------------
        # Splitter
        # -----------------------------------------------------

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.setObjectName(
            "userSplitter"
        )

        splitter.addWidget(
            form_widget
        )

        splitter.addWidget(
            self.table
        )

        splitter.setSizes(
            [
                380,
                820,
            ]
        )

        form_widget.setMinimumWidth(
            330
        )

        self.table.setMinimumWidth(
            500
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
            self.toggle_active
        )

        self.table.user_selected.connect(
            self.edit_selected
        )

    # =========================================================
    # LOAD ROLES
    # =========================================================

    def load_roles(self) -> None:

        roles = (
            self._role_repository.get_all()
        )

        self.form.load_roles(
            roles
        )

    # =========================================================
    # LOAD USERS
    # =========================================================

    def load_users(self) -> None:

        users = (
            self._user_service.get_all()
        )

        self.table.set_users(
            users
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save(self) -> None:

        data = self.form.get_data()

        password = data.pop(
            "password"
        )

        if data["role_id"] is None:

            QMessageBox.warning(
                self,
                "Error",
                "Please select a role.",
            )

            return

        try:

            if self._selected_user_id is None:

                if not password:

                    QMessageBox.warning(
                        self,
                        "Error",
                        "Password cannot be empty.",
                    )

                    return

                self._user_service.create(
                    password=password,
                    **data,
                )

                self.show_information(
                    "User created successfully."
                )

            else:

                self._user_service.update(
                    self._selected_user_id,
                    password=(
                        password
                        if password
                        else None
                    ),
                    **data,
                )

                self.show_information(
                    "User updated successfully."
                )

            self.clear_form()
            self.load_users()

        except (
            InvalidUsernameError,
            InvalidFullNameError,
            InvalidPasswordError,
            InvalidEmailError,
            UserAlreadyExistsError,
            RoleNotFoundError,
            UserNotFoundError,
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
        user: User,
    ) -> None:

        if user.id is None:
            return

        self._selected_user_id = (
            user.id
        )

        self.form.set_data(
            username=user.username,
            full_name=user.full_name,
            email=user.email,
            role_id=user.role_id,
        )

        self.form.set_edit_mode()

        self.delete_button.setText(
            "Deactivate"
            if user.is_active
            else "Activate"
        )

    # =========================================================
    # ACTIVATE / DEACTIVATE
    # =========================================================

    def toggle_active(self) -> None:

        user = (
            self.table.selected_user()
        )

        if user is None:
            return

        if user.id is None:
            return

        if user.is_active:

            if not self.ask_confirmation(
                "Deactivate User",
                f'Deactivate "{user.username}"?',
            ):
                return

            try:

                self._user_service.deactivate(
                    user.id
                )

            except UserNotFoundError as error:

                QMessageBox.warning(
                    self,
                    "Error",
                    str(error),
                )

                return

        else:

            if not self.ask_confirmation(
                "Activate User",
                f'Activate "{user.username}"?',
            ):
                return

            try:

                self._user_service.activate(
                    user.id
                )

            except UserNotFoundError as error:

                QMessageBox.warning(
                    self,
                    "Error",
                    str(error),
                )

                return

        self.clear_form()
        self.load_users()

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_form(self) -> None:

        self._selected_user_id = None

        self.form.clear()

        self.form.set_create_mode()

        self.delete_button.setText(
            "Deactivate"
        )