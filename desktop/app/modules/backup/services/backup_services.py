from datetime import datetime
from pathlib import Path
import sqlite3

from app.core.config import settings


class BackupService:
    """
    Creates, validates, restores, and manages
    SQLite database backups.
    """

    def __init__(
        self,
        database_path: Path | None = None,
        backup_dir: Path | None = None,
    ) -> None:

        self._database_path = (
            database_path
            if database_path is not None
            else settings.database_path
        )

        self._backup_dir = (
            backup_dir
            if backup_dir is not None
            else settings.backup_dir
        )

    # =========================================================
    # CREATE BACKUP
    # =========================================================

    def create_backup(self) -> Path:

        if not self._database_path.exists():

            raise FileNotFoundError(
                "Database file was not found."
            )

        self._backup_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        backup_path = (
            self._backup_dir
            / f"inventory_backup_{timestamp}.db"
        )

        source = None
        destination = None

        try:

            source = sqlite3.connect(
                self._database_path
            )

            destination = sqlite3.connect(
                backup_path
            )

            with destination:

                source.backup(
                    destination
                )

        except Exception:

            if backup_path.exists():
                backup_path.unlink()

            raise

        finally:

            if source is not None:
                source.close()

            if destination is not None:
                destination.close()

        self._validate_backup(
            backup_path
        )

        self.cleanup_old_backups(
            keep=10
        )

        return backup_path

    # =========================================================
    # VALIDATE DATABASE
    # =========================================================

    def _validate_backup(
        self,
        backup_path: Path,
    ) -> None:

        connection = None

        try:

            connection = sqlite3.connect(
                backup_path
            )

            result = connection.execute(
                "PRAGMA integrity_check;"
            ).fetchone()

            if not result or result[0] != "ok":

                raise RuntimeError(
                    "Database integrity check failed."
                )

        finally:

            if connection is not None:
                connection.close()

    # =========================================================
    # VALIDATE BACKUP PATH
    # =========================================================

    def _validate_backup_path(
        self,
        backup_path: Path,
    ) -> None:

        backup_path = backup_path.resolve()

        backup_dir = (
            self._backup_dir.resolve()
        )

        if backup_path.parent != backup_dir:

            raise ValueError(
                "The selected file is not inside "
                "the backup directory."
            )

        if not backup_path.is_file():

            raise FileNotFoundError(
                "Backup file was not found."
            )

        if backup_path.suffix.lower() != ".db":

            raise ValueError(
                "The selected file is not a database backup."
            )

    # =========================================================
    # RESTORE BACKUP
    # =========================================================

    def restore_backup(
        self,
        backup_path: Path,
    ) -> None:
        """
        Restore a selected backup as the active database.

        The application database connection must already
        be closed before this method is called.
        """

        self._validate_backup_path(
            backup_path
        )

        self._validate_backup(
            backup_path
        )

        temporary_database = (
            self._database_path.with_suffix(
                ".restore.db"
            )
        )

        if temporary_database.exists():

            temporary_database.unlink()

        source = None
        destination = None

        try:

            source = sqlite3.connect(
                backup_path
            )

            destination = sqlite3.connect(
                temporary_database
            )

            with destination:

                source.backup(
                    destination
                )

        finally:

            if source is not None:
                source.close()

            if destination is not None:
                destination.close()

        try:

            self._validate_backup(
                temporary_database
            )

            temporary_database.replace(
                self._database_path
            )

        except Exception:

            if temporary_database.exists():
                temporary_database.unlink()

            raise

    # =========================================================
    # BACKUP DIRECTORY
    # =========================================================

    def get_backup_directory(self) -> Path:

        return self._backup_dir

    # =========================================================
    # LIST BACKUPS
    # =========================================================

    def get_backups(self) -> list[Path]:

        if not self._backup_dir.exists():
            return []

        return sorted(
            (
                path
                for path in self._backup_dir.glob(
                    "inventory_backup_*.db"
                )
                if path.is_file()
            ),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )

    # =========================================================
    # DELETE BACKUP
    # =========================================================

    def delete_backup(
        self,
        backup_path: Path,
    ) -> None:

        self._validate_backup_path(
            backup_path
        )

        backup_path.unlink()

    # =========================================================
    # CLEAN OLD BACKUPS
    # =========================================================

    def cleanup_old_backups(
        self,
        keep: int = 10,
    ) -> list[Path]:

        if keep < 1:

            raise ValueError(
                "keep must be at least 1."
            )

        backups = self.get_backups()

        old_backups = backups[keep:]

        for backup in old_backups:
            backup.unlink()

        return old_backups