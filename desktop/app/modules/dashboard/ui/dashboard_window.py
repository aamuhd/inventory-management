from __future__ import annotations
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from app.core.session.current_session import CurrentSession



class DashboardWindow(QMainWindow):
    def __init__(self, current_session: CurrentSession) -> None:
        super().__init__()

        self._current_session = current_session

        self.setWindowTitle("Inventory Management System")
        self.resize(1200, 700)

        self._build_ui()

    def _build_ui(self) -> None:
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        root_layout = QVBoxLayout(central_widget)

        # Header
        header = QLabel(
            f"Welcome, {self._current_session.user.full_name}"
        )
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        root_layout.addWidget(header)

        # Main Layout
        main_layout = QHBoxLayout()

        # Sidebar
        sidebar = QVBoxLayout()

        buttons = [
            "Dashboard",
            "Categories",
            "Products",
            "Sales",
            "Users",
            "Reports",
            "Backup",
            "Settings",
            "Logout",
        ]

        for text in buttons:
            button = QPushButton(text)
            button.setMinimumHeight(40)
            sidebar.addWidget(button)

        sidebar.addStretch()

        # Content
        content = QLabel("Dashboard")
        content.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addLayout(sidebar, 1)
        main_layout.addWidget(content, 4)

        root_layout.addLayout(main_layout)

        self.setStatusBar(QStatusBar())