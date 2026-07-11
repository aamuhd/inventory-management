from app.core.config import settings


def main() -> None:
    print("=" * 50)
    print(settings.app_name)
    print(f"Version : {settings.app_version}")
    print(f"Database: {settings.database_path}")
    print(f"API URL : {settings.api_base_url}")
    print("=" * 50)


if __name__ == "__main__":
    main()