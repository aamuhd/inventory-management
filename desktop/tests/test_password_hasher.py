import pytest
from sqlmodel import Session, SQLModel, select

from app.core.database.manager import DatabaseManager
from app.core.security.password_hasher import PasswordHasher
from app.modules.authentication.models.role import Role
from app.modules.authentication.models.user import User
from app.modules.authentication.repositories.user_repository import UserRepository
from app.modules.authentication.services.authentication_service import AuthenticationService


@pytest.fixture
def session():
    database_manager = DatabaseManager()
    engine = database_manager.engine
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    # Optional: drop tables after tests if desired
    # SQLModel.metadata.drop_all(engine)


@pytest.fixture
def hasher():
    return PasswordHasher()


@pytest.fixture
def repository(session):
    return UserRepository(session)


@pytest.fixture
def service(repository, hasher):
    return AuthenticationService(repository, hasher)


def test_authenticate_admin_user(session, hasher, repository, service):
    # Create role if it doesn't exist
    admin = session.exec(
            select(Role).where(Role.name == "Admin")
        ).first()

    if admin is None:
        admin = Role(name="Admin")
        session.add(admin)
        commit()

    # Create test user
    user = session.exec(
            select(User).where(User.username == "admin")
        ).first()
    if user is None:
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

    assert authenticated_user is not None
    assert authenticated_user.username == "admin"