from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application configuration loaded from the .env file.
    """

    app_name: str = Field(default="Inventory Management System")
    app_version: str = Field(default="1.0.0")

    database_name: str = Field(default="inventory.db")
    database_dir: Path = Field(default=Path("data"))

    log_dir: Path = Field(default=Path("logs"))
    backup_dir: Path = Field(default=Path("backups"))

    api_base_url: str = Field(default="http://127.0.0.1:8000")

    sync_interval: int = Field(default=30)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def database_path(self) -> Path:
        return self.database_dir / self.database_name


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """
    Returns a cached Settings instance.
    """
    return Settings()