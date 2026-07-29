from app.modules.authentication.services.authentication_service import AuthenticationService
from app.core.session.current_session import CurrentSession
from app.modules.authentication.ui.login_window import LoginWindow
from app.modules.dashboard.ui.dashboard_window import DashboardWindow
from app.core.application.navigation import Navigation
from app.modules.inventory.services.category_service import CategoryService
from app.modules.inventory.services.product_service import ProductService
from app.modules.inventory.services.product_variant_service import ProductVariantService
from app.modules.inventory.services.purchase_order_service import PurchaseOrderService
from app.modules.inventory.services.supplier_return_service import SupplierReturnService
from app.modules.inventory.services.supplier_service import SupplierService
from app.modules.inventory.ui.category_window import CategoryWindow
from app.modules.inventory.ui.product_window import ProductWindow
from app.modules.inventory.ui.purchase_order_window import PurchaseOrderWindow
from app.modules.inventory.ui.supplier_return_window import SupplierReturnWindow
from app.modules.inventory.ui.supplier_window import SupplierWindow


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
    ):

        self._authentication_service = authentication_service
        self._current_session = current_session
        self._category_service = category_service
        self._product_service = product_service
        self._variant_service = variant_service
        self._supplier_service = supplier_service
        self._purchase_order_service = purchase_order_service
        self._supplier_return_service = supplier_return_service

        self._login_window = None
        self._dashboard_window = None
        self._category_window = None
        self._product_window = None
        self._supplier_window = None
        self._purchase_order_window = None
        self._supplier_return_window = None

        if self._category_window is not None:
            self._category_window.destroyed.connect(
                lambda: setattr(self, "_category_window", None),
            )

    def show_login(self) -> None:
        if self._dashboard_window:
            self._dashboard_window.close()

        self._login_window = LoginWindow(
            navigation=self,
            authentication_service=self._authentication_service,
            current_session=self._current_session,
        )

        self._login_window.show()

    def show_dashboard(self) -> None:
        if self._login_window:
            self._login_window.close()

        self._dashboard_window = DashboardWindow(
            navigation=self,
            current_session=self._current_session,
        )

        self._dashboard_window.show()

    def show_categories(self) -> None:

        if self._category_window is None:

            self._category_window = CategoryWindow(
                category_service=self._category_service,
            )

        self._category_window.show()
        self._category_window.raise_()
        self._category_window.activateWindow()

    def show_products(self) -> None:

        if self._product_window is None:
            self._product_window = ProductWindow(
                product_service=self._product_service,
                category_service=self._category_service,
            )
        self._product_window.show()
        self._product_window.raise_()
        self._product_window.activateWindow()

    def show_suppliers(self) -> None:

        if self._supplier_window is None:
            self._supplier_window = SupplierWindow(
                supplier_service=self._supplier_service,
            )
        self._supplier_window.show()
        self._supplier_window.raise_()
        self._supplier_window.activateWindow()

    def show_purchase_orders(self) -> None:

        if self._purchase_order_window is None:
            self._purchase_order_window = PurchaseOrderWindow(
                purchase_order_service=self._purchase_order_service,
                supplier_service=self._supplier_service,
                variant_service=self._variant_service,
            )

        self._purchase_order_window.show()
        self._purchase_order_window.raise_()
        self._purchase_order_window.activateWindow()

    def show_supplier_returns(self) -> None:

        if self._supplier_return_window is None:
            self._supplier_return_window = SupplierReturnWindow(
                supplier_return_service=self._supplier_return_service,
                supplier_service=self._supplier_service,
                purchase_order_service=self._purchase_order_service,
                variant_service=self._variant_service,
            )

        self._supplier_return_window.show()
        self._supplier_return_window.raise_()
        self._supplier_return_window.activateWindow()