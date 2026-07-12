from loguru import logger as loguru_logger

from app.core.config import settings


class LoggerManager:
    """
    Configures and provides access to the application logger.
    """

    def __init__(self) -> None:
        self._configured = False

    def configure(self) -> None:
        """Configure Loguru only once."""
        if self._configured:
            return

        loguru_logger.remove()

        # Console output
        loguru_logger.add(
            sink=lambda message: print(message, end=""),
            level="INFO",
        )

        # File output
        loguru_logger.add(
            settings.log_dir / "application.log",
            rotation="10 MB",
            retention="30 days",
            level="INFO",
            enqueue=True,
            backtrace=True,
            diagnose=True,
        )

        self._configured = True

    @property
    def logger(self):
        """Return the configured Loguru logger."""
        return loguru_logger