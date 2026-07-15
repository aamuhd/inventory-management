from app.core.filesystem import DirectoryManager
from app.core.logging import LoggerManager
from app.core.database.manager import DatabaseManager
from sqlmodel import SQLModel, Session
from app.modules.authentication.repositories.user_repository import UserRepository
from app.core.security.password_hasher import PasswordHasher
from app.modules.authentication.services.authentication_service import AuthenticationService
from app.core.session.current_session import CurrentSession
from PySide6.QtWidgets import QApplication

import sys

from app.core.application.application_controller import ApplicationController
from app.modules.authentication.ui.login_window import LoginWindow



def main() -> None:
    DirectoryManager().prepare()

    logger_manager = LoggerManager()
    logger_manager.configure()

    logger = logger_manager.logger

    logger.info("Application started successfully.")

    app = QApplication(sys.argv)

    database_manager = DatabaseManager()

    SQLModel.metadata.create_all(database_manager.engine)

    session = Session(database_manager.engine)

    user_repository = UserRepository(session)

    password_hasher = PasswordHasher()

    authentication_service = AuthenticationService(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )

    current_session = CurrentSession()

    window = LoginWindow(
    authentication_service=authentication_service,
    current_session=current_session,
)

    window.show()

    sys.exit(app.exec())
        


if __name__ == "__main__":
    main()
    
