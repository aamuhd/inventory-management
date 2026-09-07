from sqlmodel import Session, select

from app.modules.base_repo import BaseRepository
from app.modules.settings.models.settings import Settings


class SettingsRepository(BaseRepository):
    """
    Handles database operations for application settings.

    The application uses one settings record identified by
    the DEFAULT_KEY.
    """

    DEFAULT_KEY = "default"

    def __init__(
        self,
        session: Session,
    ) -> None:
        super().__init__(session)

    # =========================================================
    # GET
    # =========================================================

    def get(self) -> Settings | None:
        """
        Return the application's settings record.
        """

        statement = (
            select(Settings)
            .where(
                Settings.key == self.DEFAULT_KEY
            )
        )

        return self._session.exec(
            statement
        ).first()

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self,
        settings: Settings,
    ) -> Settings:
        """
        Create the application's settings record.
        """

        settings.key = self.DEFAULT_KEY

        self._session.add(settings)

        self._commit()

        self._session.refresh(settings)

        return settings

    # =========================================================
    # UPDATE
    # =========================================================

    def update(
        self,
        settings: Settings,
    ) -> Settings:
        """
        Update the application's settings record.
        """

        self._session.add(settings)

        self._commit()

        self._session.refresh(settings)

        return settings
