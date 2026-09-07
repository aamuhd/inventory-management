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

from app.modules.authentication.models.role import Role


class RoleTable(QWidget):

    role_selected = Signal(Role)

    def __init__(self) -> None:

        super().__init__()

        self._roles: list[Role] = []

        self._roles_by_id: dict = {}

        self.setObjectName(
            "roleTableContainer"
        )

        self._build_ui()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        self.table = QTableWidget()

        self.table.setObjectName(
            "roleTable"
        )

        self.table.setSortingEnabled(
            True
        )

        self.table.setColumnCount(
            4
        )

        self.table.setHorizontalHeaderLabels(
            [
                "Name",
                "Description",
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

    def set_roles(
        self,
        roles: list[Role],
    ) -> None:

        self._roles = list(
            roles
        )

        self._roles_by_id = {
            role.id: role
            for role in roles
            if role.id is not None
        }

        sorting_enabled = (
            self.table.isSortingEnabled()
        )

        self.table.setSortingEnabled(
            False
        )

        self.table.clearContents()

        self.table.setRowCount(
            len(roles)
        )

        for row, role in enumerate(roles):

            name_item = QTableWidgetItem(
                role.name
            )

            if role.id is not None:
                name_item.setData(
                    Qt.ItemDataRole.UserRole,
                    role.id,
                )

            self.table.setItem(
                row,
                0,
                name_item,
            )

            self.table.setItem(
                row,
                1,
                QTableWidgetItem(
                    role.description or ""
                ),
            )

            status = (
                "Active"
                if role.is_active
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
                2,
                status_item,
            )

            created = (
                role.created_at.strftime(
                    "%Y-%m-%d %H:%M"
                )
            )

            self.table.setItem(
                row,
                3,
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

    def selected_role(
        self,
    ) -> Role | None:

        row = self.table.currentRow()

        if row < 0:
            return None

        item = self.table.item(
            row,
            0,
        )

        if item is None:
            return None

        role_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if role_id is None:
            return None

        return self._roles_by_id.get(
            role_id
        )

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self) -> None:

        self._roles.clear()

        self._roles_by_id.clear()

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

        role = self.selected_role()

        if role is not None:

            self.role_selected.emit(
                role
            )