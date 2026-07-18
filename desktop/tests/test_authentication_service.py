from app.core.security.password_hasher import PasswordHasher   # adjust import if needed


def test_password_hashing_and_verification():
    hasher = PasswordHasher()
    password = "ChangeMe123!"

    password_hash = hasher.hash_password(password)

    assert hasher.verify_password(password, password_hash) is True
    assert hasher.verify_password("wrong-password", password_hash) is False


def test_password_hash_is_not_plaintext():
    hasher = PasswordHasher()
    password = "ChangeMe123!"

    password_hash = hasher.hash_password(password)

    assert password != password_hash
    assert len(password_hash) > 20