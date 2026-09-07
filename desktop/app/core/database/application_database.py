from sqlmodel import Session

from app.core.database.manager import DatabaseManager


class ApplicationDatabase:

    def __init__(
        self,
        database_manager: DatabaseManager,
    ) -> None:

        self._database_manager = (
            database_manager
        )

        self._session = Session(
            database_manager.engine
        )

    @property
    def session(self) -> Session:

        return self._session

    @property
    def database_manager(
        self,
    ) -> DatabaseManager:

        return self._database_manager

    def close(self) -> None:

        self._session.close()

        self._database_manager.dispose()