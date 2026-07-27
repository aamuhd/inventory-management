from sqlmodel import Session, select

from app.core.database.manager import DatabaseManager
from app.core.security.password_hasher import PasswordHasher
from app.modules.authentication.models.role import Role
from app.modules.authentication.models.user import User
from app.modules.authentication.repositories.user_repository import UserRepository
from app.modules.authentication.services.authentication_service import AuthenticationService


database_manager = DatabaseManager()
engine = database_manager.engine

from sqlmodel import SQLModel


SQLModel.metadata.create_all(engine)

def main():
    with Session(engine) as session:
        hasher = PasswordHasher()
        repository = UserRepository(session)
        service = AuthenticationService(repository, hasher)

        # Create role if it doesn't exist
        admin = session.exec(
            select(Role).where(Role.name == "Admin")
        ).first()

        if admin is None:
            admin = Role(name="Admin")
            session.add(admin)
            session.commit()

        # Create test user
        user = User(
            username="admin",
            full_name="Administrator",
            password_hash=hasher.hash_password("ChangeMe123!"),
            role_id=admin.id,
        )

        repository.create(user)

        authenticated_user = service.authenticate(
            "admin",
            "ChangeMe123!",
        )

        print(authenticated_user.username)
        print("success")


if __name__ == "__main__":
    main()