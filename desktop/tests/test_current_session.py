from app.core.session.current_session import CurrentSession
from app.modules.authentication.models.user import User

def test_current_session():
    session = CurrentSession()

    assert not session.is_authenticated

    user = User(
        username="admin",
        full_name="System Administrator",
        password_hash="dummy_hash",
        role_id="00000000-0000-0000-0000-000000000000",
    )

    session.login(user)
    

    assert session.is_authenticated
    assert session.user.username == "admin"

    session.logout()

    assert not session.is_authenticated