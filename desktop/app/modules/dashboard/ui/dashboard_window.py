from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from app.core.application.navigation import Navigation
from app.core.session.current_session import CurrentSession

from app.modules.dashboard.ui.dashboard_widget import DashboardWidget
from app.modules.reports.services.report_service import ReportService

from app.modules.settings.services.settings_service import SettingsService


class DashboardWindow(QMainWindow):

    def __init__(
        self,
        navigation: Navigation,
        current_session: CurrentSession,
        report_service: ReportService,
        settings_service: SettingsService
    ) -> None:

        super().__init__()

        self._navigation = navigation
        self._current_session = current_session
        self._report_service = report_service
        self._settings_service = settings_service

        settings = self._settings_service.get()

        print("Business name:", repr(settings.business_name))

        self.setWindowTitle(
            settings.business_name if settings.business_name else "Inventory Management System"
        )

        self.resize(
            1200,
            700,
        )

        self._build_ui()
        self._connect_signals()

    # =========================================================
    # UI
    # =========================================================

    def _build_ui(self) -> None:

        central_widget = QWidget()

        central_widget.setObjectName(
            "dashboardWindow"
        )

        self.setCentralWidget(
            central_widget
        )

        root_layout = QVBoxLayout(
            central_widget
        )

        # =====================================================
        # HEADER
        # =====================================================

        user_name = (
            self._current_session.user.full_name
            if self._current_session.user
            else "User"
        )

        header = QLabel(
            f"Welcome, {user_name}"
        )

        header.setObjectName(
            "dashboardHeader"
        )

        header.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        header.setMinimumHeight(
            45
        )

        root_layout.addWidget(
            header
        )

        # =====================================================
        # MAIN CONTENT
        # =====================================================

        main_layout = QHBoxLayout()

        # =====================================================
        # SIDEBAR
        # =====================================================

        sidebar_container = QWidget()

        sidebar_container.setObjectName(
            "dashboardSidebar"
        )

        sidebar_container.setMinimumWidth(
            220
        )

        sidebar_container.setMaximumWidth(
            280
        )

        sidebar_layout = QVBoxLayout(
            sidebar_container
        )

        sidebar_layout.setContentsMargins(
            5,
            5,
            5,
            5,
        )

        sidebar_layout.setSpacing(
            5
        )

        # =====================================================
        # DASHBOARD
        # =====================================================

        self.dashboard_button = (
            self._create_main_button(
                "Dashboard"
            )
        )

        sidebar_layout.addWidget(
            self.dashboard_button
        )

        # =====================================================
        # INVENTORY
        # =====================================================

        self.inventory_button = (
            self._create_main_button(
                "Inventory  ▾"
            )
        )

        sidebar_layout.addWidget(
            self.inventory_button
        )

        self.inventory_menu = QWidget()

        inventory_layout = QVBoxLayout(
            self.inventory_menu
        )

        inventory_layout.setContentsMargins(
            15,
            0,
            0,
            0,
        )

        inventory_layout.setSpacing(
            3
        )

        self.category_button = (
            self._create_sub_button(
                "Categories"
            )
        )

        self.product_button = (
            self._create_sub_button(
                "Products"
            )
        )

        self.product_variants_button = (
            self._create_sub_button(
                "Product Variants"
            )
        )

        self.supplier_button = (
            self._create_sub_button(
                "Suppliers"
            )
        )

        self.purchase_order_button = (
            self._create_sub_button(
                "Purchase Orders"
            )
        )

        self.supplier_return_button = (
            self._create_sub_button(
                "Supplier Returns"
            )
        )

        inventory_buttons = [
            self.category_button,
            self.product_button,
            self.product_variants_button,
            self.supplier_button,
            self.purchase_order_button,
            self.supplier_return_button,
        ]

        for button in inventory_buttons:
            inventory_layout.addWidget(
                button
            )

        self.inventory_menu.setVisible(
            False
        )

        sidebar_layout.addWidget(
            self.inventory_menu
        )

        # =====================================================
        # SALES
        # =====================================================

        self.sales_button = (
            self._create_main_button(
                "Sales  ▾"
            )
        )

        sidebar_layout.addWidget(
            self.sales_button
        )

        self.sales_menu = QWidget()

        sales_layout = QVBoxLayout(
            self.sales_menu
        )

        sales_layout.setContentsMargins(
            15,
            0,
            0,
            0,
        )

        sales_layout.setSpacing(
            3
        )

        self.sale_button = (
            self._create_sub_button(
                "Sales"
            )
        )

        self.sales_return_button = (
            self._create_sub_button(
                "Sales Returns"
            )
        )

        self.customer_button = (
            self._create_sub_button(
                "Customers"
            )
        )

        sales_buttons = [
            self.sale_button,
            self.sales_return_button,
            self.customer_button,
        ]

        for button in sales_buttons:
            sales_layout.addWidget(
                button
            )

        self.sales_menu.setVisible(
            False
        )

        sidebar_layout.addWidget(
            self.sales_menu
        )

        # =====================================================
        # REPORTS
        # =====================================================

        self.reports_button = (
            self._create_main_button(
                "Reports  ▾"
            )
        )

        sidebar_layout.addWidget(
            self.reports_button
        )

        self.reports_menu = QWidget()

        reports_layout = QVBoxLayout(
            self.reports_menu
        )

        reports_layout.setContentsMargins(
            15,
            0,
            0,
            0,
        )

        reports_layout.setSpacing(
            3
        )

        self.report_button = (
            self._create_sub_button(
                "Reports"
            )
        )

        reports_layout.addWidget(
            self.report_button
        )

        self.reports_menu.setVisible(
            False
        )

        sidebar_layout.addWidget(
            self.reports_menu
        )

        # =====================================================
        # USERS
        # =====================================================

        self.user_button = (
            self._create_main_button(
                "Users  ▾"
            )
        )

        sidebar_layout.addWidget(
            self.user_button
        )

        self.user_menu = QWidget()

        user_layout = QVBoxLayout(
            self.user_menu
        )

        user_layout.setContentsMargins(
            15,
            0,
            0,
            0,
        )

        user_layout.setSpacing(
            3
        )

        self.users_button = (
            self._create_sub_button(
                "Users"
            )
        )

        self.roles_button = (
            self._create_sub_button(
                "Roles"
            )
        )

        user_layout.addWidget(
            self.users_button
        )

        user_layout.addWidget(
            self.roles_button
        )

        self.user_menu.setVisible(
            False
        )

        sidebar_layout.addWidget(
            self.user_menu
        )

        # =====================================================
        # OTHER MAIN BUTTONS
        # =====================================================

        self.backup_button = (
            self._create_main_button(
                "Backup"
            )
        )

        self.settings_button = (
            self._create_main_button(
                "Settings"
            )
        )

        sidebar_layout.addWidget(
            self.backup_button
        )

        sidebar_layout.addWidget(
            self.settings_button
        )

        # =====================================================
        # SPACER
        # =====================================================

        sidebar_layout.addStretch()

        # =====================================================
        # LOGOUT
        # =====================================================

        self.logout_button = (
            self._create_main_button(
                "Logout"
            )
        )

        sidebar_layout.addWidget(
            self.logout_button
        )

        # =====================================================
        # SIDEBAR SCROLL
        # =====================================================

        sidebar_scroll = QScrollArea()

        sidebar_scroll.setWidgetResizable(
            True
        )

        sidebar_scroll.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        sidebar_scroll.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        sidebar_scroll.setWidget(
            sidebar_container
        )

        # =====================================================
        # DASHBOARD WIDGET
        # =====================================================

        self.dashboard_widget = DashboardWidget(
            report_service=self._report_service,
        )

        self.dashboard_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        # =====================================================
        # MAIN LAYOUT
        # =====================================================

        main_layout.addWidget(
            sidebar_scroll,
            1,
        )

        main_layout.addWidget(
            self.dashboard_widget,
            4,
        )

        root_layout.addLayout(
            main_layout
        )

        # =====================================================
        # STATUS BAR
        # =====================================================

        self.setStatusBar(
            QStatusBar()
        )

    # =========================================================
    # BUTTON FACTORIES
    # =========================================================

    @staticmethod
    def _create_main_button(
        text: str,
    ) -> QPushButton:

        button = QPushButton(text)

        button.setObjectName(
            "mainNavigationButton"
        )

        button.setProperty(
            "navButton",
            True,
        )

        button.setMinimumHeight(
            42
        )

        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        return button

    @staticmethod
    def _create_sub_button(
        text: str,
    ) -> QPushButton:

        button = QPushButton(text)

        button.setObjectName(
            "subNavigationButton"
        )

        button.setProperty(
            "subButton",
            True,
        )

        button.setMinimumHeight(
            36
        )

        button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        return button

    # =========================================================
    # SIGNALS
    # =========================================================

    def _connect_signals(self) -> None:

        # -----------------------------------------------------
        # Dashboard
        # -----------------------------------------------------

        self.dashboard_button.clicked.connect(
            self._navigation.show_dashboard
        )

        # -----------------------------------------------------
        # Inventory
        # -----------------------------------------------------

        self.inventory_button.clicked.connect(
            self._toggle_inventory
        )

        self.category_button.clicked.connect(
            self._navigation.show_categories
        )

        self.product_button.clicked.connect(
            self._navigation.show_products
        )

        self.product_variants_button.clicked.connect(
            self._navigation.show_product_variants
        )

        self.supplier_button.clicked.connect(
            self._navigation.show_suppliers
        )

        self.purchase_order_button.clicked.connect(
            self._navigation.show_purchase_orders
        )

        self.supplier_return_button.clicked.connect(
            self._navigation.show_supplier_returns
        )

        # -----------------------------------------------------
        # Sales
        # -----------------------------------------------------

        self.sales_button.clicked.connect(
            self._toggle_sales
        )

        self.sale_button.clicked.connect(
            self._navigation.show_sales
        )

        self.sales_return_button.clicked.connect(
            self._navigation.show_sales_returns
        )

        self.customer_button.clicked.connect(
            self._navigation.show_customers
        )

        # -----------------------------------------------------
        # Reports
        # -----------------------------------------------------

        self.reports_button.clicked.connect(
            self._toggle_reports
        )

        self.report_button.clicked.connect(
            self._navigation.show_reports
        )

        # -----------------------------------------------------
        # Users
        # -----------------------------------------------------

        self.user_button.clicked.connect(
            self._toggle_users
        )

        self.roles_button.clicked.connect(
            self._navigation.show_roles
        )

        self.users_button.clicked.connect(
            self._navigation.show_users
        )

        # -----------------------------------------------------
        # Backup
        # -----------------------------------------------------

        self.backup_button.clicked.connect(
            self._navigation.show_backup
        )

        # -----------------------------------------------------
        # Settings
        # -----------------------------------------------------

        self.settings_button.clicked.connect(
            self._navigation.show_settings
        )

        # -----------------------------------------------------
        # Logout
        # -----------------------------------------------------

        self.logout_button.clicked.connect(
            self.logout
        )

    # =========================================================
    # TOGGLE INVENTORY
    # =========================================================

    def _toggle_inventory(self) -> None:

        visible = (
            self.inventory_menu.isVisible()
        )

        self.inventory_menu.setVisible(
            not visible
        )

        self.inventory_button.setText(
            "Inventory  ▴"
            if not visible
            else "Inventory  ▾"
        )

    # =========================================================
    # TOGGLE SALES
    # =========================================================

    def _toggle_sales(self) -> None:

        visible = (
            self.sales_menu.isVisible()
        )

        self.sales_menu.setVisible(
            not visible
        )

        self.sales_button.setText(
            "Sales  ▴"
            if not visible
            else "Sales  ▾"
        )

    # =========================================================
    # TOGGLE REPORTS
    # =========================================================

    def _toggle_reports(self) -> None:

        visible = (
            self.reports_menu.isVisible()
        )

        self.reports_menu.setVisible(
            not visible
        )

        self.reports_button.setText(
            "Reports  ▴"
            if not visible
            else "Reports  ▾"
        )

    # =========================================================
    # TOGGLE USERS
    # =========================================================

    def _toggle_users(self) -> None:

        visible = (
            self.user_menu.isVisible()
        )

        self.user_menu.setVisible(
            not visible
        )

        self.user_button.setText(
            "Users  ▴"
            if not visible
            else "Users  ▾"
        )

    # =========================================================
    # LOGOUT
    # =========================================================

    def logout(self) -> None:

        reply = QMessageBox.question(
            self,
            "Logout",
            "Are you sure you want to logout?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
        )

        if (
            reply
            != QMessageBox.StandardButton.Yes
        ):
            return

        self._current_session.logout()

        self.close()

        self._navigation.show_login()

    # =========================================================
    # REFRESH
    # =========================================================

    def refresh_dashboard(self) -> None:
        self.dashboard_widget.refresh()
