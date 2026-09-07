import os
from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)


def get_application_data_dir() -> Path:
    """
    Return the directory where application data should be stored.

    Windows:
        C:\\Users\\<user>\\AppData\\Local\\Inventory Management System

    Linux:
        ~/.local/share/Inventory Management System
    """

    # =========================================================
    # WINDOWS
    # =========================================================

    if os.name == "nt":

        local_app_data = os.environ.get(
            "LOCALAPPDATA"
        )

        if local_app_data:

            return (
                Path(local_app_data)
                / "Inventory Management System"
            )

        return (
            Path.home()
            / "AppData"
            / "Local"
            / "Inventory Management System"
        )

    # =========================================================
    # LINUX / OTHER UNIX SYSTEMS
    # =========================================================

    xdg_data_home = os.environ.get(
        "XDG_DATA_HOME"
    )

    if xdg_data_home:

        return (
            Path(xdg_data_home)
            / "Inventory Management System"
        )

    return (
        Path.home()
        / ".local"
        / "share"
        / "Inventory Management System"
    )


class Settings(BaseSettings):
    """
    Application configuration loaded from the .env file.
    """

    app_name: str = Field(
        default="Inventory Management System"
    )

    app_version: str = Field(
        default="1.0.0"
    )

    database_name: str = Field(
        default="inventory.db"
    )

    database_dir: Path = Field(
        default_factory=get_application_data_dir
    )

    log_dir: Path = Field(
        default_factory=lambda:
            get_application_data_dir() / "logs"
    )

    backup_dir: Path = Field(
        default_factory=lambda:
            get_application_data_dir() / "backups"
    )

    api_base_url: str = Field(
        default="http://127.0.0.1:8000"
    )

    sync_interval: int = Field(
        default=30
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_path(self) -> Path:

        return (
            self.database_dir
            / self.database_name
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """

    return Settings()
