from pathlib import Path

from app.core.config import settings


class DirectoryManager:
    """
    Creates and manages the application's required directories.
    """

    def __init__(self) -> None:
        self.directories = [
            settings.database_dir,
            settings.log_dir,
            settings.backup_dir,
        ]

    def prepare(self) -> None:
        """
        Create all required directories if they do not exist.
        """
        for directory in self.directories:
            directory.mkdir(parents=True, exist_ok=True)