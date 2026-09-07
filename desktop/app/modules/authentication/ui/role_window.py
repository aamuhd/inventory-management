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
    InvalidRoleNameError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)

from app.modules.authentication.models.role import Role

from app.modules.authentication.services.role_service import (
    RoleService,
)

from app.modules.authentication.ui.role_form import (
    RoleForm,
)

from app.modules.authentication.ui.role_table import (
    RoleTable,
)


class RoleWindow(BaseWindow):

    def __init__(
        self,
        role_service: RoleService,
    ) -> None:

        super().__init__()

        self._role_service = role_service

        self._selected_role_id: UUID | None = None

        self._build_ui()
        self._connect_signals()

        self.load_roles()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.setWindowTitle(
            "Role Management"
        )

        self.setObjectName(
            "roleWindow"
        )

        self.setMinimumSize(
            850,
            500,
        )

        self.resize(
            1100,
            650,
        )

        # -----------------------------------------------------
        # Form
        # -----------------------------------------------------

        self.form = RoleForm()

        self.toggle_button = QPushButton(
            "Deactivate"
        )

        self.toggle_button.setObjectName(
            "roleToggleButton"
        )

        self.toggle_button.setMinimumHeight(
            40
        )

        self.toggle_button.setCursor(
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
            self.toggle_button
        )

        form_widget = QWidget()

        form_widget.setObjectName(
            "roleFormContainer"
        )

        form_widget.setLayout(
            form_layout
        )

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        self.table = RoleTable()

        # -----------------------------------------------------
        # Splitter
        # -----------------------------------------------------

        splitter = QSplitter(
            Qt.Orientation.Horizontal
        )

        splitter.setObjectName(
            "roleSplitter"
        )

        splitter.addWidget(
            form_widget
        )

        splitter.addWidget(
            self.table
        )

        splitter.setSizes(
            [
                360,
                740,
            ]
        )

        form_widget.setMinimumWidth(
            300
        )

        self.table.setMinimumWidth(
            450
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

        self.toggle_button.clicked.connect(
            self.toggle_active
        )

        self.table.role_selected.connect(
            self.edit_selected
        )

    # =========================================================
    # LOAD
    # =========================================================

    def load_roles(self) -> None:

        roles = (
            self._role_service.get_all()
        )

        self.table.set_roles(
            roles
        )

    # =========================================================
    # SAVE
    # =========================================================

    def save(self) -> None:

        data = self.form.get_data()

        try:

            if self._selected_role_id is None:

                self._role_service.create(
                    **data
                )

                self.show_information(
                    "Role created successfully."
                )

            else:

                self._role_service.update(
                    self._selected_role_id,
                    **data,
                )

                self.show_information(
                    "Role updated successfully."
                )

            self.clear_form()

            self.load_roles()

        except (
            InvalidRoleNameError,
            RoleAlreadyExistsError,
            RoleNotFoundError,
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
        role: Role,
    ) -> None:

        if role.id is None:
            return

        self._selected_role_id = (
            role.id
        )

        self.form.set_data(
            name=role.name,
            description=role.description,
        )

        self.form.set_edit_mode()

        self.toggle_button.setText(
            "Deactivate"
            if role.is_active
            else "Activate"
        )

    # =========================================================
    # ACTIVATE / DEACTIVATE
    # =========================================================

    def toggle_active(self) -> None:

        role = (
            self.table.selected_role()
        )

        if role is None:
            return

        if role.id is None:
            return

        if role.is_active:

            if not self.ask_confirmation(
                "Deactivate Role",
                f'Deactivate "{role.name}"?',
            ):
                return

            try:

                self._role_service.deactivate(
                    role.id
                )

            except RoleNotFoundError as error:

                QMessageBox.warning(
                    self,
                    "Error",
                    str(error),
                )

                return

        else:

            if not self.ask_confirmation(
                "Activate Role",
                f'Activate "{role.name}"?',
            ):
                return

            try:

                self._role_service.activate(
                    role.id
                )

            except RoleNotFoundError as error:

                QMessageBox.warning(
                    self,
                    "Error",
                    str(error),
                )

                return

        self.clear_form()

        self.load_roles()

    # =========================================================
    # CLEAR
    # =========================================================

    def clear_form(self) -> None:

        self._selected_role_id = None

        self.form.clear()

        self.form.set_create_mode()

        self.toggle_button.setText(
            "Deactivate"
        )