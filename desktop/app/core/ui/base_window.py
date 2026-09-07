from __future__ import annotations

from PySide6.QtWidgets import (
    QMessageBox,
    QSizePolicy,
    QWidget,
)


class BaseWindow(QWidget):

    def __init__(
        self,
    ) -> None:
        super().__init__()

        self._setup_window()

    # =========================================================
    # WINDOW SETUP
    # =========================================================

    def _setup_window(self) -> None:

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        self.setMinimumSize(
            800,
            500,
        )

    # =========================================================
    # MESSAGE BOX
    # =========================================================

    def _create_message_box(
        self,
        title: str,
        message: str,
        icon: QMessageBox.Icon,
    ) -> QMessageBox:

        box = QMessageBox(self)

        box.setWindowTitle(title)

        box.setIcon(icon)

        box.setText(message)

        # Allow the message text to wrap instead of
        # forcing the entire message box to become very wide.
        box.setSizePolicy(
            QSizePolicy.Policy.Preferred,
            QSizePolicy.Policy.Preferred,
        )

        return box

    # =========================================================
    # ERROR
    # =========================================================

    def show_error(
        self,
        message: str,
    ) -> None:

        box = self._create_message_box(
            "Error",
            message,
            QMessageBox.Icon.Critical,
        )

        box.exec()

    # =========================================================
    # INFORMATION
    # =========================================================

    def show_information(
        self,
        message: str,
    ) -> None:

        box = self._create_message_box(
            "Info",
            message,
            QMessageBox.Icon.Information,
        )

        box.exec()

    # =========================================================
    # CONFIRMATION
    # =========================================================

    def ask_confirmation(
        self,
        title: str,
        message: str,
    ) -> bool:

        box = self._create_message_box(
            title,
            message,
            QMessageBox.Icon.Question,
        )

        box.setStandardButtons(
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No
        )

        return (
            box.exec()
            == QMessageBox.StandardButton.Yes
        )