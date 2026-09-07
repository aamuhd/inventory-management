from sqlmodel import create_engine

from app.core.config import settings


class DatabaseManager:
    """
    Responsible for creating and managing the database engine.
    """

    def __init__(self) -> None:

        self._engine = create_engine(
            f"sqlite:///{settings.database_path}",
            echo=False,
            connect_args={
                "check_same_thread": False,
            },
        )

    # =========================================================
    # ENGINE
    # =========================================================

    @property
    def engine(self):
        return self._engine

    # =========================================================
    # DISPOSE
    # =========================================================

    def dispose(self) -> None:
        """
        Close all connections held by the database engine.
        """

        self._engine.dispose()