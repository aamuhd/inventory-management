from uuid import UUID

from sqlalchemy.orm import selectinload
from sqlmodel import Session, select, col

from app.modules.authentication.models.user import User


class UserRepository:
    """Repository for User database operations."""

    def __init__(
        self,
        session: Session,
    ) -> None:

        self._session = session

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self,
        user: User,
    ) -> User:

        self._session.add(user)

        self._session.flush()
        self._session.refresh(user)

        return user

    # =========================================================
    # GET
    # =========================================================

    def get_by_id(
        self,
        user_id: UUID,
    ) -> User | None:

        statement = (
            select(User)
            .where(User.id == user_id)
        )

        return self._session.exec(
            statement
        ).first()

    def get_by_username(
        self,
        username: str,
    ) -> User | None:

        statement = (
            select(User)
            .where(User.username == username)
        )

        return self._session.exec(
            statement
        ).first()

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = (
            select(User)
            .where(User.email == email)
        )

        return self._session.exec(
            statement
        ).first()

    def get_all(
        self,
    ) -> list[User]:

        statement = (
            select(User)
            .options(
                selectinload(User.role)
            )
            .order_by(User.username)
        )

        return list(
            self._session.exec(
                statement
            )
        )

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        user: User,
    ) -> User:

        self._session.add(user)

        self._session.flush()
        self._session.refresh(user)

        return user

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        user: User,
    ) -> None:

        self._session.delete(user)

        self._session.flush()