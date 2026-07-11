from app.core.config import settings
from app.core.filesystem import DirectoryManager


def main() -> None:
    manager = DirectoryManager()
    manager.prepare()

    print(f"Application : {settings.app_name}")
    print(f"Database    : {settings.database_path}")
    print("Directories are ready.")


if __name__ == "__main__":
    main()