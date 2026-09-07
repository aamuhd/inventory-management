from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session


class BaseRepository:

    def __init__(
        self,
        session: Session,
    ) -> None:
        self._session = session

    def _commit(self) -> None:
        try:
            self._session.commit()
        except SQLAlchemyError:
            self._session.rollback()
            raise