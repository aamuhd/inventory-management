from collections.abc import Callable
from pathlib import Path

from app.modules.authentication.services.authentication_service import (
    AuthenticationService,
)
from app.core.session.current_session import CurrentSession
from app.modules.authentication.ui.login_window import LoginWindow
from app.modules.dashboard.ui.dashboard_window import DashboardWindow
from app.core.application.navigation import Navigation

from app.modules.authentication.repositories.role_repository import (
    RoleRepository,
)
from app.modules.authentication.services.user_service import (
    UserService,
)
from app.modules.authentication.ui.user_window import UserWindow

from app.modules.inventory.services.category_service import CategoryService
from app.modules.inventory.services.product_service import ProductService
from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)
from app.modules.inventory.services.purchase_order_service import (
    PurchaseOrderService,
)
from app.modules.inventory.services.supplier_return_service import (
    SupplierReturnService,
)
from app.modules.inventory.services.supplier_service import SupplierService

from app.modules.inventory.ui.category_window import CategoryWindow
from app.modules.inventory.ui.product_window import ProductWindow
from app.modules.inventory.ui.purchase_order_window import (
    PurchaseOrderWindow,
)
from app.modules.inventory.ui.supplier_return_window import (
    SupplierReturnWindow,
)
from app.modules.inventory.ui.supplier_window import SupplierWindow
from app.modules.inventory.ui.product_variant_window import (
    ProductVariantWindow,
)

from app.modules.sales.ui.customer_window import CustomerWindow
from app.modules.sales.ui.customer_detail_window import (
    CustomerDetailWindow,
)
from app.modules.sales.models.customer import Customer
from app.modules.sales.services.customer_service import CustomerService
from app.modules.sales.ui.sale_window import SaleWindow
from app.modules.sales.services.sale_service import SaleService
from app.modules.sales.services.sale_return_service import (
    SalesReturnService,
)
from app.modules.sales.services.sale_item_service import SaleItemService
from app.modules.sales.ui.sales_return_window import SalesReturnWindow

from app.modules.reports.services.report_service import ReportService
from app.modules.reports.ui.report_window import ReportsWindow

from app.modules.authentication.services.role_service import RoleService
from app.modules.authentication.ui.role_window import RoleWindow

from app.modules.backup.services.backup_services import BackupService
from app.modules.backup.ui.backup_window import BackupWindow

from app.modules.settings.services.settings_service import (
    SettingsService,
)
from app.modules.settings.ui.settings_window import (
    SettingsWindow,
)
from app.modules.sales.services.payment_service import PaymentService

from app.modules.authentication.ui.change_password_window import (
    ChangePasswordWindow,
)

from app.modules.authentication.services.password_recovery_service import (
    PasswordRecoveryService,
)

from app.modules.authentication.ui.password_recovery_window import (
    PasswordRecoveryWindow,
)


class ApplicationController(Navigation):

    def __init__(
        self,
        authentication_service: AuthenticationService,
        current_session: CurrentSession,
        category_service: CategoryService,
        product_service: ProductService,
        variant_service: ProductVariantService,
        supplier_service: SupplierService,
        purchase_order_service: PurchaseOrderService,
        supplier_return_service: SupplierReturnService,
        customer_service: CustomerService,
        sale_service: SaleService,
        sales_return_service: SalesReturnService,
        sale_item_service: SaleItemService,
        report_service: ReportService,
        user_service: UserService,
        role_repository: RoleRepository,
        role_service: RoleService,
        backup_service: BackupService,
        settings_service: SettingsService,
        payment_service: PaymentService,
        password_recovery_service: PasswordRecoveryService,
        restore_and_restart: Callable[[Path], None],
    ) -> None:

        self._authentication_service = (
            authentication_service
        )

        self._current_session = current_session

        self._category_service = category_service
        self._product_service = product_service
        self._variant_service = variant_service
        self._supplier_service = supplier_service

        self._purchase_order_service = (
            purchase_order_service
        )

        self._supplier_return_service = (
            supplier_return_service
        )

        self._customer_service = customer_service
        self._sale_service = sale_service

        self._sales_return_service = (
            sales_return_service
        )

        self._sale_item_service = sale_item_service
        self._report_service = report_service
        self._role_service = role_service

        self._backup_service = backup_service

        self._settings_service = settings_service

        self._payment_service = payment_service

        self._restore_and_restart = (
            restore_and_restart
        )

        # -----------------------------------------------------
        # User module
        # -----------------------------------------------------

        self._user_service = user_service
        self._role_repository = role_repository

        self._password_recovery_service = (
            password_recovery_service
        )
        

        # -----------------------------------------------------
        # Windows
        # -----------------------------------------------------

        self._login_window = None
        self._dashboard_window = None
        self._category_window = None
        self._product_window = None
        self._supplier_window = None
        self._purchase_order_window = None
        self._supplier_return_window = None
        self._product_variant_window = None
        self._customer_window = None
        self._customer_detail_window = None
        self._sale_window = None
        self._sales_return_window = None
        self._report_window = None
        self._user_window = None
        self._role_window = None
        self._backup_window = None
        self._settings_window = None
        self._change_password_window = None
        self._password_recovery_window = None

    # =========================================================
    # WINDOW HELPER
    # =========================================================

    def _show_window(
        self,
        attribute_name: str,
        factory,
    ) -> None:

        window = getattr(
            self,
            attribute_name,
        )

        if window is None:

            window = factory()

            setattr(
                self,
                attribute_name,
                window,
            )

            window.destroyed.connect(
                lambda _,
                name=attribute_name: setattr(
                    self,
                    name,
                    None,
                )
            )

        window.show()
        window.raise_()
        window.activateWindow()

    # =========================================================
    # LOGIN
    # =========================================================

    def show_login(self) -> None:

        if self._dashboard_window:
            self._dashboard_window.close()

        self._login_window = LoginWindow(
            navigation=self,
            authentication_service=(
                self._authentication_service
            ),
            current_session=self._current_session,
        )

        self._login_window.show()

    # =========================================================
    # PASSWORD RECOVERY
    # =========================================================

    def show_password_recovery(self) -> None:

        self._show_window(
            "_password_recovery_window",
            lambda: PasswordRecoveryWindow(
                navigation=self,
                password_recovery_service=(
                    self._password_recovery_service
                ),
            ),
        )

    # =========================================================
    # CHANGE PASSWORD
    # =========================================================

    def show_change_password(self) -> None:

        self._show_window(
            "_change_password_window",
            lambda: ChangePasswordWindow(
                navigation=self,
                current_session=self._current_session,
                user_service=self._user_service,
            ),
        )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self) -> None:

        if self._login_window:
            self._login_window.close()

        self._dashboard_window = DashboardWindow(
            navigation=self,
            current_session=self._current_session,
            report_service=self._report_service,
            settings_service=self._settings_service,
        )

        self._dashboard_window.show()

    def refresh_dashboard(self) -> None:

        if self._dashboard_window is None:
            return

        self._dashboard_window.refresh_dashboard()

    # =========================================================
    # CATEGORIES
    # =========================================================

    def show_categories(self) -> None:

        self._show_window(
            "_category_window",
            lambda: CategoryWindow(
                category_service=self._category_service,
                refresh_products=(
                    self.refresh_products
                ),
            ),
        )

    # =========================================================
    # PRODUCTS
    # =========================================================

    def show_products(self) -> None:

        self._show_window(
            "_product_window",
            lambda: ProductWindow(
                product_service=self._product_service,
                category_service=self._category_service,
                refresh_product_variants=(
                    self.refresh_product_variants
                ),
            ),
        )

    # =========================================================
    # REFRESH PRODUCTS
    # =========================================================

    def refresh_products(self) -> None:

        if self._product_window is None:
            return

        self._product_window.refresh_categories()

    # =========================================================
    # SUPPLIERS
    # =========================================================

    def show_suppliers(self) -> None:

        self._show_window(
            "_supplier_window",
            lambda: SupplierWindow(
                supplier_service=self._supplier_service,
            ),
        )

    # =========================================================
    # PURCHASE ORDERS
    # =========================================================

    def show_purchase_orders(self) -> None:

        self._show_window(
            "_purchase_order_window",
            lambda: PurchaseOrderWindow(
                purchase_order_service=(
                    self._purchase_order_service
                ),
                supplier_service=self._supplier_service,
                variant_service=self._variant_service,
                refresh_dashboard=self.refresh_dashboard,
            ),
        )

    # =========================================================
    # SUPPLIER RETURNS
    # =========================================================

    def show_supplier_returns(self) -> None:

        self._show_window(
            "_supplier_return_window",
            lambda: SupplierReturnWindow(
                supplier_return_service=(
                    self._supplier_return_service
                ),
                supplier_service=self._supplier_service,
                purchase_order_service=(
                    self._purchase_order_service
                ),
                variant_service=self._variant_service,
            ),
        )

    # =========================================================
    # PRODUCT VARIANTS
    # =========================================================

    def show_product_variants(self) -> None:

        self._show_window(
            "_product_variant_window",
            lambda: ProductVariantWindow(
                variant_service=self._variant_service,
                product_service=self._product_service,
            ),
        )

    # =========================================================
    # REFRESH PRODUCT VARIANTS
    # =========================================================

    def refresh_product_variants(self) -> None:

        if self._product_variant_window is not None:
            self._product_variant_window.refresh()

    # =========================================================
    # CUSTOMERS
    # =========================================================

    def show_customers(self) -> None:

        self._show_window(
            "_customer_window",
            lambda: CustomerWindow(
                customer_service=self._customer_service,
                refresh_sale_customers=(
                    self.refresh_sale_customers
                ),
                show_customer_details=(
                    self.show_customer_detail
                ),
            ),
        )

        # =========================================================
    # CUSTOMER DETAIL
    # =========================================================

    def show_customer_detail(
        self,
        customer: Customer,
    ) -> None:

        # -----------------------------------------------------
        # Close existing customer detail window
        # -----------------------------------------------------

        if self._customer_detail_window is not None:

            self._customer_detail_window.close()

            self._customer_detail_window = None

        # -----------------------------------------------------
        # Create new window
        # -----------------------------------------------------

        window = CustomerDetailWindow(
            customer=customer,
            sale_service=self._sale_service,
            payment_service=self._payment_service,
            settings_service=self._settings_service,
        )

        # -----------------------------------------------------
        # Clear reference when this window is destroyed
        # -----------------------------------------------------

        window.destroyed.connect(
            lambda _=None,
            window=window: (
                setattr(
                    self,
                    "_customer_detail_window",
                    None,
                )
                if self._customer_detail_window is window
                else None
            )
        )

        # -----------------------------------------------------
        # Store the new window
        # -----------------------------------------------------

        self._customer_detail_window = window

        # -----------------------------------------------------
        # Show window
        # -----------------------------------------------------

        window.show()
        window.raise_()
        window.activateWindow()

    # =========================================================
    # REFRESH SALE CUSTOMERS
    # =========================================================

    def refresh_sale_customers(self) -> None:

        if self._sale_window is None:
            return

        self._sale_window.refresh_customers()

    # =========================================================
    # SALES
    # =========================================================

    def show_sales(self) -> None:

        self._show_window(
            "_sale_window",
            lambda: SaleWindow(
                sale_service=self._sale_service,
                customer_service=self._customer_service,
                variant_service=self._variant_service,
                payment_service=self._payment_service,
                refresh_product_variants=(
                    self.refresh_product_variants
                ),
                refresh_dashboard=self.refresh_dashboard,
            ),
        )

    # =========================================================
    # SALES RETURNS
    # =========================================================

    def show_sales_returns(self) -> None:

        self._show_window(
            "_sales_return_window",
            lambda: SalesReturnWindow(
                sales_return_service=(
                    self._sales_return_service
                ),
                sale_service=self._sale_service,
                sale_item_service=self._sale_item_service,
            ),
        )

    # =========================================================
    # REPORTS
    # =========================================================

    def show_reports(self) -> None:

        self._show_window(
            "_report_window",
            lambda: ReportsWindow(
                report_service=self._report_service,
            ),
        )

    # =========================================================
    # ROLES
    # =========================================================

    def show_roles(self) -> None:

        self._show_window(
            "_role_window",
            lambda: RoleWindow(
                role_service=self._role_service,
            ),
        )

    # =========================================================
    # USERS
    # =========================================================

    def show_users(self) -> None:

        self._show_window(
            "_user_window",
            lambda: UserWindow(
                user_service=self._user_service,
                role_repository=self._role_repository,
            ),
        )

    # =========================================================
    # BACKUP
    # =========================================================

    def show_backup(self) -> None:

        self._show_window(
            "_backup_window",
            lambda: BackupWindow(
                backup_service=self._backup_service,
                restore_and_restart=(
                    self._restore_and_restart
                ),
            ),
        )

    # =========================================================
    # SETTINGS
    # =========================================================

    def show_settings(self) -> None:

        self._show_window(
            "_settings_window",
            lambda: SettingsWindow(
                settings_service=self._settings_service,
            ),
        )

    # =========================================================
    # PREPARE FOR DATABASE RESTORE
    # =========================================================

    def prepare_for_database_restore(self) -> None:
        """
        Close application windows before the database connection
        is closed and the database is replaced.
        """

        windows = [
            self._dashboard_window,
            self._category_window,
            self._product_window,
            self._supplier_window,
            self._purchase_order_window,
            self._supplier_return_window,
            self._product_variant_window,
            self._customer_window,
            self._customer_detail_window,
            self._sale_window,
            self._sales_return_window,
            self._report_window,
            self._user_window,
            self._role_window,
            self._backup_window,
            self._settings_window,
            self._change_password_window,
            self._password_recovery_window,
        ]

        for window in windows:

            if window is not None:
                window.close()