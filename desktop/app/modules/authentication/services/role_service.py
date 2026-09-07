from uuid import UUID

from app.modules.authentication.exceptions import (
    InvalidRoleNameError,
    RoleAlreadyExistsError,
    RoleNotFoundError,
)

from app.modules.authentication.models.role import Role

from app.modules.authentication.repositories.role_repository import (
    RoleRepository,
)


class RoleService:

    def __init__(
        self,
        repository: RoleRepository,
    ) -> None:

        self._repository = repository

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self,
        *,
        name: str,
        description: str | None = None,
    ) -> Role:

        name = name.strip()

        if not name:
            raise InvalidRoleNameError(
                "Role name cannot be empty."
            )

        existing = self._repository.get_by_name(
            name
        )

        if existing is not None:
            raise RoleAlreadyExistsError(
                f'Role "{name}" already exists.'
            )

        if description is not None:
            description = description.strip()

        role = Role(
            name=name,
            description=description,
        )

        return self._repository.create(
            role
        )

    # =========================================================
    # GET
    # =========================================================

    def get_by_id(
        self,
        role_id: UUID,
    ) -> Role:

        role = self._repository.get_by_id(
            role_id
        )

        if role is None:
            raise RoleNotFoundError(
                "Role not found."
            )

        return role

    def get_all(self) -> list[Role]:

        return self._repository.get_all()

    def get_active(self) -> list[Role]:

        return [
            role
            for role in self.get_all()
            if role.is_active
        ]

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        role_id: UUID,
        *,
        name: str,
        description: str | None = None,
    ) -> Role:

        role = self.get_by_id(
            role_id
        )

        name = name.strip()

        if not name:
            raise InvalidRoleNameError(
                "Role name cannot be empty."
            )

        existing = self._repository.get_by_name(
            name
        )

        if (
            existing is not None
            and existing.id != role.id
        ):
            raise RoleAlreadyExistsError(
                f'Role "{name}" already exists.'
            )

        if description is not None:
            description = description.strip()

        role.sqlmodel_update(
            {
                "name": name,
                "description": description,
            }
        )

        return self._repository.update(
            role
        )

    # =========================================================
    # ACTIVATE / DEACTIVATE
    # =========================================================

    def set_active(
        self,
        role_id: UUID,
        is_active: bool,
    ) -> Role:

        role = self.get_by_id(
            role_id
        )

        role.is_active = is_active

        return self._repository.update(
            role
        )

    def activate(
        self,
        role_id: UUID,
    ) -> Role:

        return self.set_active(
            role_id,
            True,
        )

    def deactivate(
        self,
        role_id: UUID,
    ) -> Role:

        return self.set_active(
            role_id,
            False,
        )