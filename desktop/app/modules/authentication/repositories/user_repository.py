from uuid import UUID

from sqlmodel import Session, select

from app.modules.authentication.models.user import User


class UserRepository:
    """Repository for User database operations."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, user: User) -> User:
        self._session.add(user)
        self._commit()
        self._session.refresh(user)
        return user

    def get_by_id(self, user_id: UUID) -> User | None:
        statement = select(User).where(User.id == user_id)
        return self._session.exec(statement).first()

    def get_by_username(self, username: str) -> User | None:
        statement = select(User).where(User.username == username)
        return self._session.exec(statement).first()

    def update(self, user: User) -> User:
        self._session.add(user)
        self._commit()
        self._session.refresh(user)
        return user