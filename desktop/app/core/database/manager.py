from sqlmodel import SQLModel, create_engine

from app.core.config import settings


class DatabaseManager:
    """
    Responsible for creating and providing the database engine.
    """

    def __init__(self) -> None:
        self._engine = create_engine(
            f"sqlite:///{settings.database_path}",
            echo=False,
            connect_args={"check_same_thread": False},
        )

    @property
    def engine(self):
        return self._engine