from __future__ import annotations

from PySide6.QtWidgets import (
    QWidget,
    QMainWindow,
    QMessageBox,

)


class BaseWindow(QWidget):

    def __init__(
        self,
    ) -> None:
        super().__init__()

    def show_error(
        self,
        message: str,
    ) -> None:

        QMessageBox.critical(
            self,
            "Error",
            message,
        )

    def show_information(
        self,
        message: str,
    ) -> None:

        QMessageBox.information(
            self,
            "Information",
            message,
        )

    def ask_confirmation(
        self,
        title: str,
        message: str,
    ) -> bool:

        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        return (
            reply
            == QMessageBox.StandardButton.Yes
        )