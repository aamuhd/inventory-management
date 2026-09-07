from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
)

from app.core.ui.base_window import BaseWindow
from app.modules.backup.services.backup_services import (
    BackupService,
)


class BackupWindow(BaseWindow):

    def __init__(
        self,
        backup_service: BackupService,
        restore_and_restart,
    ) -> None:

        super().__init__()

        self._backup_service = (
            backup_service
        )

        self._restore_and_restart = (
            restore_and_restart
        )

        self.setWindowTitle(
            "Database Backup"
        )

        self.setObjectName(
            "backupWindow"
        )

        self.setMinimumSize(
            650,
            450,
        )

        self.resize(
            750,
            500,
        )

        self._build_ui()

        self.load_backups()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        title = QLabel(
            "Database Backup"
        )

        title.setObjectName(
            "backupTitle"
        )

        description = QLabel(
            "Create a backup of your inventory database."
        )

        description.setObjectName(
            "backupDescription"
        )

        self.location_label = QLabel()

        self.location_label.setObjectName(
            "backupLocation"
        )

        self.backup_count_label = QLabel()

        self.backup_count_label.setObjectName(
            "backupCountLabel"
        )

        self.backup_button = QPushButton(
            "Create Backup"
        )

        self.backup_button.setObjectName(
            "backupCreateButton"
        )

        self.backup_button.setMinimumHeight(
            42
        )

        self.backup_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.restore_button = QPushButton(
            "Restore Selected Backup"
        )

        self.restore_button.setObjectName(
            "backupRestoreButton"
        )

        self.restore_button.setMinimumHeight(
            42
        )

        self.restore_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.refresh_button = QPushButton(
            "Refresh"
        )

        self.refresh_button.setObjectName(
            "backupRefreshButton"
        )

        self.refresh_button.setMinimumHeight(
            42
        )

        self.refresh_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.backup_list = QListWidget()

        self.backup_list.setObjectName(
            "backupList"
        )

        buttons_layout = QHBoxLayout()

        buttons_layout.setSpacing(
            8
        )

        buttons_layout.addWidget(
            self.backup_button
        )

        buttons_layout.addWidget(
            self.restore_button
        )

        buttons_layout.addWidget(
            self.refresh_button
        )

        layout = QVBoxLayout(
            self
        )

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        layout.setSpacing(
            12
        )

        layout.addWidget(
            title
        )

        layout.addWidget(
            description
        )

        layout.addWidget(
            self.location_label
        )

        layout.addWidget(
            self.backup_count_label
        )

        layout.addLayout(
            buttons_layout
        )

        layout.addWidget(
            self.backup_list
        )

        self.backup_button.clicked.connect(
            self.create_backup
        )

        self.restore_button.clicked.connect(
            self.restore_selected_backup
        )

        self.refresh_button.clicked.connect(
            self.load_backups
        )

        self._update_location()

    # =========================================================
    # LOCATION
    # =========================================================

    def _update_location(self) -> None:

        location = (
            self._backup_service
            .get_backup_directory()
        )

        self.location_label.setText(
            f"Backup location: {location.resolve()}"
        )

    # =========================================================
    # LOAD BACKUPS
    # =========================================================

    def load_backups(self) -> None:

        self.backup_list.clear()

        backups = (
            self._backup_service
            .get_backups()
        )

        self.backup_count_label.setText(
            f"Available backups: {len(backups)}"
        )

        if not backups:

            item = QListWidgetItem(
                "No backups found."
            )

            item.setFlags(
                Qt.ItemFlag.NoItemFlags
            )

            self.backup_list.addItem(
                item
            )

            return

        for backup in backups:

            size = backup.stat().st_size

            size_kb = size / 1024

            item = QListWidgetItem(
                f"{backup.name}   "
                f"({size_kb:.1f} KB)"
            )

            item.setData(
                Qt.ItemDataRole.UserRole,
                str(backup),
            )

            self.backup_list.addItem(
                item
            )

    # =========================================================
    # CREATE BACKUP
    # =========================================================

    def create_backup(self) -> None:

        self.backup_button.setEnabled(
            False
        )

        try:

            backup_path = (
                self._backup_service
                .create_backup()
            )

            QMessageBox.information(
                self,
                "Backup Successful",
                (
                    "Database backup created successfully.\n\n"
                    f"{backup_path}"
                ),
            )

            self.load_backups()

        except Exception as error:

            QMessageBox.critical(
                self,
                "Backup Failed",
                (
                    "The database backup could not be created.\n\n"
                    f"{error}"
                ),
            )

        finally:

            self.backup_button.setEnabled(
                True
            )

    # =========================================================
    # RESTORE SELECTED BACKUP
    # =========================================================

    def restore_selected_backup(self) -> None:

        item = self.backup_list.currentItem()

        if item is None:

            QMessageBox.warning(
                self,
                "Restore Backup",
                "Please select a backup first.",
            )

            return

        backup_path = item.data(
            Qt.ItemDataRole.UserRole
        )

        if not backup_path:

            QMessageBox.warning(
                self,
                "Restore Backup",
                "The selected backup is invalid.",
            )

            return

        backup_path = Path(
            backup_path
        )

        reply = QMessageBox.warning(
            self,
            "Restore Backup",
            (
                "Restoring this backup will replace the "
                "current database.\n\n"
                "The application will close and restart "
                "after the restore.\n\n"
                "All changes made after this backup was "
                "created will be lost.\n\n"
                "Are you sure you want to continue?"
            ),
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if (
            reply
            != QMessageBox.StandardButton.Yes
        ):
            return

        self.restore_button.setEnabled(
            False
        )

        self.backup_button.setEnabled(
            False
        )

        self.refresh_button.setEnabled(
            False
        )

        try:

            # -------------------------------------------------
            # Application-level restore
            # -------------------------------------------------

            self._restore_and_restart(
                backup_path
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Restore Failed",
                (
                    "The database could not be restored.\n\n"
                    f"{error}"
                ),
            )

            self.restore_button.setEnabled(
                True
            )

            self.backup_button.setEnabled(
                True
            )

            self.refresh_button.setEnabled(
                True
            )