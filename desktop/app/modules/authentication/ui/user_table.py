from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QAbstractItemView,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from app.modules.authentication.models.user import User


class UserTable(QWidget):

    user_selected = Signal(User)

    def __init__(self) -> None:

        super().__init__()

        self._users: list[User] = []

        self._users_by_id: dict = {}

        self.setObjectName(
            "userTableContainer"
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.table = QTableWidget()

        self.table.setObjectName(
            "userTable"
        )

        self.table.setSortingEnabled(
            True
        )

        self.table.setColumnCount(
            6
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Username",
                "Full Name",
                "Email",
                "Role",
                "Status",
                "Created",
            ]
        )

        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )

        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )

        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setWordWrap(
            False
        )

        self.table.verticalHeader().setVisible(
            False
        )

        self.table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            QHeaderView.ResizeMode.Interactive
        )

        header.setMinimumSectionSize(
            100
        )

        header.setStretchLastSection(
            True
        )

        self.table.itemDoubleClicked.connect(
            self._on_item_double_clicked
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            self.table
        )

    # =========================================================
    # DATA
    # =========================================================

    def set_users(
        self,
        users: list[User],
    ) -> None:

        self._users = list(
            users
        )

        self._users_by_id = {
            user.id: user
            for user in users
            if user.id is not None
        }

        sorting_enabled = (
            self.table.isSortingEnabled()
        )

        self.table.setSortingEnabled(
            False
        )

        self.table.clearContents()

        self.table.setRowCount(
            len(users)
        )

        for row, user in enumerate(users):

            username_item = QTableWidgetItem(
                user.username
            )

            if user.id is not None:
                username_item.setData(
                    Qt.ItemDataRole.UserRole,
                    user.id,
                )

            self.table.setItem(
                row,
                0,
                username_item,
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    user.full_name
                ),
            )

            self.table.setItem(
                row,
                2,
                QTableWidgetItem(
                    user.email or ""
                ),
            )

            role_name = ""

            if user.role is not None:
                role_name = user.role.name

            self.table.setItem(
                row,
                3,
                QTableWidgetItem(
                    role_name
                ),
            )

            status = (
                "Active"
                if user.is_active
                else "Inactive"
            )

            status_item = QTableWidgetItem(
                status
            )

            status_item.setTextAlignment(
                Qt.AlignmentFlag.AlignCenter
                | Qt.AlignmentFlag.AlignVCenter
            )

            self.table.setItem(
                row,
                4,
                status_item,
            )

            created = (
                user.created_at.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

            self.table.setItem(
                row,
                5,
                QTableWidgetItem(
                    created
                ),
            )

        self.table.setSortingEnabled(
            sorting_enabled
        )

    # =========================================================
    # SELECTION
    # =========================================================

    def selected_user(
        self,
    ) -> User | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(
            row,
            0,
        )

        if item is None:
            return None

        user_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if user_id is None:
            return None

        return self._users_by_id.get(
            user_id
        )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self._users.clear()
        self._users_by_id.clear()

        self.table.clearContents()

        self.table.setRowCount(
            0
        )

    # =========================================================
    # EVENTS
    # =========================================================

    def _on_item_double_clicked(
        self,
        item: QTableWidgetItem,
    ) -> None:

        user = self.selected_user()

        if user is not None:

            self.user_selected.emit(
                user
            )