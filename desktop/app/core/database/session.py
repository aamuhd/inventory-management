from sqlmodel import Session

from .manager import DatabaseManager


class SessionManager:
    """
    Creates database sessions.
    """

    def __init__(self, database: DatabaseManager) -> None:
        self._database = database

    def create_session(self) -> Session:
        return Session(self._database.engine)