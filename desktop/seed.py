from sqlmodel import Session, select

from app.core.database.application_database import DatabaseManager
from app.core.security.password_hasher import PasswordHasher

from app.modules.authentication.models.role import Role
from app.modules.authentication.models.user import User

from app.modules.authentication.repositories.user_repository import (
    UserRepository,
)

from app.modules.authentication.services.authentication_service import (
    AuthenticationService,
)


database_manager = DatabaseManager()
engine = database_manager.engine

from sqlmodel import SQLModel


SQLModel.metadata.create_all(engine)


def main():

    with Session(engine) as session:

        hasher = PasswordHasher()

        repository = UserRepository(
            session
        )

        service = AuthenticationService(
            repository,
            hasher,
        )

        # =====================================================
        # CREATE ADMIN ROLE
        # =====================================================

        admin = session.exec(
            select(Role).where(
                Role.name == "Admin"
            )
        ).first()

        if admin is None:

            admin = Role(
                name="Admin"
            )

            session.add(
                admin
            )

            session.commit()

            session.refresh(
                admin
            )

        # =====================================================
        # CREATE DEFAULT ADMIN USER
        # =====================================================

        existing_user = session.exec(
            select(User).where(
                User.username == "admin"
            )
        ).first()

        if existing_user is None:

            user = User(
                username="admin",
                full_name="Chairman Textile",
                password_hash=(
                    hasher.hash_password(
                        "ChangeMe123!"
                    )
                ),
                role_id=admin.id,

                # -------------------------------------------------
                # Force the administrator to change the default
                # password on the first login.
                # -------------------------------------------------

                must_change_password=True,
            )

            repository.create(
                user
            )

            session.commit()

        # =====================================================
        # TEST AUTHENTICATION
        # =====================================================

        
        service.authenticate(
            "admin",
            "ChangeMe123!",
        )


if __name__ == "__main__":
    main()

