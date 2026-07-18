from app.core.security.password_hasher import PasswordHasher


def test_password_hashing_and_verification():
    hasher = PasswordHasher()
    password = "ChangeMe123!"

    # Hash the password
    password_hash = hasher.hash_password(password)

    # Should verify correct password
    assert hasher.verify_password(password, password_hash) is True

    # Should reject wrong password
    assert hasher.verify_password("wrong-password", password_hash) is False


# Optional: Add more specific tests
def test_password_hash_is_not_plaintext():
    hasher = PasswordHasher()
    password = "ChangeMe123!"

    password_hash = hasher.hash_password(password)

    assert password_hash != password
    assert len(password_hash) > 20  # typical hash length
    assert password_hash.startswith("$") or "$" in password_hash  # common for bcrypt/argon2 etc.


if __name__ == "__main__":
    # This allows running with `python test_file.py` if needed
    import pytest
    pytest.main([__file__, "-v"])