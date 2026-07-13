from app.core.security.password_hasher import PasswordHasher


def main() -> None:
    hasher = PasswordHasher()

    password = "ChangeMe123!"

    password_hash = hasher.hash_password(password)

    print(password_hash)

    print(
        hasher.verify_password(
            password,
            password_hash,
        )
    )

    print(
        hasher.verify_password(
            "wrong-password",
            password_hash,
        )
    )


if __name__ == "__main__":
    main()

