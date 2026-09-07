from uuid import UUID

from sqlmodel import Session, select

from app.modules.authentication.models.role import Role
from app.modules.base_repo import BaseRepository


class RoleRepository(BaseRepository):

    def __init__(
        self,
        session: Session,
    ) -> None:

        super().__init__(
            session
        )

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self,
        role: Role,
    ) -> Role:

        self._session.add(
            role
        )

        self._session.flush()
        self._session.refresh(
            role
        )

        return role

    # =========================================================
    # GET
    # =========================================================

    def get_by_id(
        self,
        role_id: UUID,
    ) -> Role | None:

        return self._session.get(
            Role,
            role_id,
        )

    def get_by_name(
        self,
        name: str,
    ) -> Role | None:

        statement = (
            select(Role)
            .where(
                Role.name == name
            )
        )

        return self._session.exec(
            statement
        ).first()

    def get_all(
        self,
    ) -> list[Role]:

        statement = (
            select(Role)
            .order_by(
                Role.name
            )
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
        role: Role,
    ) -> Role:

        self._session.add(
            role
        )

        self._session.flush()
        self._session.refresh(
            role
        )

        return role