from app.core.filesystem import DirectoryManager
from app.core.logging import LoggerManager


def main() -> None:
    DirectoryManager().prepare()

    logger_manager = LoggerManager()
    logger_manager.configure()

    logger = logger_manager.logger

    logger.info("Application started successfully.")


if __name__ == "__main__":
    main()