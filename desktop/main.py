
import multiprocessing
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication
from sqlmodel import SQLModel

from app.core.application.application_controller import (
    ApplicationController,
)
from app.core.config import settings
from app.core.database.application_database import (
    ApplicationDatabase,
)
from app.core.database.manager import DatabaseManager
from app.core.filesystem import DirectoryManager
from app.core.logging import LoggerManager
from app.core.security.password_hasher import PasswordHasher
from app.core.session.current_session import CurrentSession
from app.core.ui.style_loader import load_stylesheet

from app.modules.authentication.repositories.role_repository import (
    RoleRepository,
)
from app.modules.authentication.repositories.user_repository import (
    UserRepository,
)
from app.modules.authentication.services.authentication_service import (
    AuthenticationService,
)
from app.modules.authentication.services.role_service import (
    RoleService,
)
from app.modules.authentication.services.user_service import (
    UserService,
)

from app.modules.inventory.repositories.category_repository import (
    CategoryRepository,
)
from app.modules.inventory.repositories.product_repository import (
    ProductRepository,
)
from app.modules.inventory.repositories.product_variant_repository import (
    ProductVariantRepository,
)
from app.modules.inventory.repositories.purchase_order_item_repository import (
    PurchaseOrderItemRepository,
)
from app.modules.inventory.repositories.purchase_order_repository import (
    PurchaseOrderRepository,
)
from app.modules.inventory.repositories.supplier_repository import (
    SupplierRepository,
)
from app.modules.inventory.repositories.supplier_return_item_repository import (
    SupplierReturnItemRepository,
)
from app.modules.inventory.repositories.supplier_return_repository import (
    SupplierReturnRepository,
)
from app.modules.inventory.repositories.stock_movement_repository import (
    StockMovementRepository,
)

from app.modules.inventory.services.category_service import (
    CategoryService,
)
from app.modules.inventory.services.product_service import (
    ProductService,
)
from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)
from app.modules.inventory.services.purchase_order_service import (
    PurchaseOrderService,
)
from app.modules.inventory.services.stock_movement_service import (
    StockMovementService,
)
from app.modules.inventory.services.supplier_return_service import (
    SupplierReturnService,
)
from app.modules.inventory.services.supplier_service import (
    SupplierService,
)

from app.modules.sales.repositories.customer_repository import (
    CustomerRepository,
)
from app.modules.sales.repositories.sale_item_repository import (
    SaleItemRepository,
)
from app.modules.sales.repositories.sale_repository import (
    SaleRepository,
)
from app.modules.sales.repositories.sales_return_item_repository import (
    SalesReturnItemRepository,
)
from app.modules.sales.repositories.sales_return_repository import (
    SalesReturnRepository,
)

from app.modules.sales.services.customer_service import (
    CustomerService,
)
from app.modules.sales.services.sale_item_service import (
    SaleItemService,
)
from app.modules.sales.services.sale_return_service import (
    SalesReturnService,
)
from app.modules.sales.services.sale_service import (
    SaleService,
)

from app.modules.reports.repositories.report_repository import (
    ReportRepository,
)
from app.modules.reports.services.report_service import (
    ReportService,
)

from app.modules.backup.services.backup_services import (
    BackupService,
)

from app.modules.settings.repositories.settings_repository import (
    SettingsRepository,
)
from app.modules.settings.services.settings_service import (
    SettingsService,
)

from app.modules.sales.repositories.sale_payment_repository import (
    SalePaymentRepository,
)

from app.modules.sales.services.payment_service import (
    PaymentService,
)

from app.modules.authentication.services.password_recovery_service import (
    PasswordRecoveryService,
)
from app.core.database.seed import seed_database

def main() -> None:

    # =========================================================
    # APPLICATION SETUP
    # =========================================================

    DirectoryManager().prepare()

    logger_manager = LoggerManager()
    logger_manager.configure()

    logger = logger_manager.logger

    logger.info(
        "Application started successfully."
    )

    app = QApplication(sys.argv)

    load_stylesheet(
        app,
        "app.qss",
        "login.qss",
        "dashboard.qss",
        "category.qss",
        "product.qss",
        "product_variant.qss",
        "supplier.qss",
        "purchase_order.qss",
        "add_purchase_order_item_dialog.qss",
        "sale.qss",
        "customer.qss",
        "customer_detail.qss",
        "user.qss",
        "role.qss",
        "backup.qss",
        "settings.qss",
        "change_password.qss",
        #"receipt.qss",
    )

    # =========================================================
    # DATABASE
    # =========================================================

    database_manager = DatabaseManager()

    SQLModel.metadata.create_all(
        database_manager.engine
    )

    seed_database(
        database_manager.engine
    )

    application_database = ApplicationDatabase(
        database_manager
    )

    session = application_database.session

    # =========================================================
    # BACKUP
    # =========================================================

    backup_service = BackupService(
        database_path=settings.database_path,
        backup_dir=settings.backup_dir,
    )

    # =========================================================
    # CONTROLLER HOLDER
    # =========================================================
    #
    # ApplicationController needs restart_application()
    # during construction.
    #
    # But restart_application() needs access to the controller
    # so that it can call:
    #
    #     controller.prepare_for_database_restore()
    #
    # Therefore we use this holder to solve the construction
    # dependency cleanly.
    #

    controller_holder: dict[
        str,
        ApplicationController | None,
    ] = {
        "controller": None,
    }

    # =========================================================
    # RESTART APPLICATION
    # =========================================================

    def restore_and_restart(
        backup_path: Path,
    ) -> None:
        """
        Close the application database, restore the selected
        backup, and restart the application.
        """

        controller = controller_holder[
            "controller"
        ]

        if controller is None:
            raise RuntimeError(
                "Application controller is not initialized."
            )

        logger.info(
            "Preparing application for database restore."
        )

        # =====================================================
        # CLOSE APPLICATION WINDOWS
        # =====================================================

        controller.prepare_for_database_restore()

        # =====================================================
        # CLOSE DATABASE CONNECTION
        # =====================================================

        application_database.close()

        logger.info(
            "Database connection closed."
        )

        # =====================================================
        # RESTORE DATABASE
        # =====================================================

        backup_service.restore_backup(
            backup_path
        )

        logger.info(
            "Database restored successfully from: %s",
            backup_path,
        )

        # =====================================================
        # RESTART APPLICATION
        # =====================================================

        app.quit()

        logger.info(
            "Restarting application."
        )

        os.execv(
            sys.executable,
            [
                sys.executable,
                *sys.argv,
            ],
        )

    # =========================================================
    # AUTHENTICATION REPOSITORIES
    # =========================================================

    user_repository = UserRepository(
        session
    )

    role_repository = RoleRepository(
        session
    )

    # =========================================================
    # INVENTORY REPOSITORIES
    # =========================================================

    category_repository = CategoryRepository(
        session
    )

    product_repository = ProductRepository(
        session
    )

    variant_repository = ProductVariantRepository(
        session
    )

    supplier_repository = SupplierRepository(
        session
    )

    purchase_order_repository = (
        PurchaseOrderRepository(
            session
        )
    )

    purchase_order_item_repository = (
        PurchaseOrderItemRepository(
            session
        )
    )

    supplier_return_repository = (
        SupplierReturnRepository(
            session
        )
    )

    supplier_return_item_repository = (
        SupplierReturnItemRepository(
            session
        )
    )

    movement_repository = (
        StockMovementRepository(
            session
        )
    )

    # =========================================================
    # SALES REPOSITORIES
    # =========================================================

    customer_repository = CustomerRepository(
        session
    )

    sale_repository = SaleRepository(
        session
    )

    sale_item_repository = SaleItemRepository(
        session
    )

    sales_return_repository = (
        SalesReturnRepository(
            session
        )
    )

    sales_return_item_repository = (
        SalesReturnItemRepository(
            session
        )
    )

    # =========================================================
    # PAYMENT REPOSITORY
    # =========================================================

    sale_payment_repository = SalePaymentRepository(
        session
    )

    # =========================================================
    # REPORT REPOSITORY
    # =========================================================

    report_repository = ReportRepository(
        session
    )

    # =========================================================
    # SETTINGS REPOSITORY 
    # =========================================================

    settings_repository = SettingsRepository(
        session
    )

    # =========================================================
    # SECURITY
    # =========================================================

    password_hasher = PasswordHasher()

    # =========================================================
    # AUTHENTICATION SERVICES
    # =========================================================

    authentication_service = AuthenticationService(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )

    role_service = RoleService(
        repository=role_repository,
    )

    user_service = UserService(
        user_repository=user_repository,
        role_repository=role_repository,
        password_hasher=password_hasher,
    )


    # =========================================================
    # INVENTORY SERVICES
    # =========================================================

    category_service = CategoryService(
        repository=category_repository,
    )

    product_service = ProductService(
        product_repository=product_repository,
    )

    supplier_service = SupplierService(
        repository=supplier_repository,
    )

    stock_movement_service = StockMovementService(
        movement_repository=movement_repository,
        variant_repository=variant_repository,
    )

    customer_service = CustomerService(
        repository=customer_repository,
    )

    product_variant_service = ProductVariantService(
        variant_repository=variant_repository,
        product_service=product_service,
        stock_movement_service=stock_movement_service,
    )

    purchase_order_service = PurchaseOrderService(
        purchase_order_repository=(
            purchase_order_repository
        ),
        purchase_order_item_repository=(
            purchase_order_item_repository
        ),
        supplier_service=supplier_service,
        product_variant_service=(
            product_variant_service
        ),
        stock_movement_service=(
            stock_movement_service
        ),
    )

    supplier_return_service = SupplierReturnService(
        return_repository=supplier_return_repository,
        item_repository=supplier_return_item_repository,
        stock_movement_service=stock_movement_service,
    )

    # =========================================================
    # SETTINGS SERVICES
    # =========================================================

    settings_service = SettingsService(
        repository=settings_repository,
        password_hasher=password_hasher,
    )

    password_recovery_service = PasswordRecoveryService(
        user_service=user_service,
        settings_service=settings_service,
    )

    # =========================================================
    # SALES SERVICES
    # =========================================================

    sale_service = SaleService(
        sale_repository=sale_repository,
        sale_item_repository=sale_item_repository,
        customer_service=customer_service,
        product_variant_service=(
            product_variant_service
        ),
        stock_movement_service=(
            stock_movement_service
        ),
        settings_service=settings_service,
    )

    sale_item_service = SaleItemService(
        repository=sale_item_repository,
        sales_return_item_repository=(
            sales_return_item_repository
        ),
    )

    sales_return_service = SalesReturnService(
        sales_return_repository=(
            sales_return_repository
        ),
        sales_return_item_repository=(
            sales_return_item_repository
        ),
        sale_service=sale_service,
        sale_item_repository=sale_item_repository,
        stock_movement_service=(
            stock_movement_service
        ),
        product_variant_service=(
            product_variant_service
        ),
    )

    payment_service = PaymentService(
        repository=sale_payment_repository,
        sale_service=sale_service,
    )

    # =========================================================
    # REPORT SERVICE
    # =========================================================

    report_service = ReportService(
        repository=report_repository,
    )

    # =========================================================
    # SESSION
    # =========================================================

    current_session = CurrentSession()

    # =========================================================
    # APPLICATION CONTROLLER
    # =========================================================

    controller = ApplicationController(
        authentication_service=authentication_service,
        current_session=current_session,

        category_service=category_service,
        product_service=product_service,
        variant_service=product_variant_service,
        supplier_service=supplier_service,
        purchase_order_service=purchase_order_service,
        supplier_return_service=supplier_return_service,

        customer_service=customer_service,
        sale_service=sale_service,
        sales_return_service=sales_return_service,
        sale_item_service=sale_item_service,

        report_service=report_service,

        user_service=user_service,
        role_repository=role_repository,
        role_service=role_service,

        backup_service=backup_service,

        settings_service=settings_service,

        payment_service=payment_service,

        password_recovery_service=password_recovery_service,

        restore_and_restart=restore_and_restart,
    )

    # =========================================================
    # STORE CONTROLLER
    # =========================================================

    controller_holder[
        "controller"
    ] = controller

    # =========================================================
    # START APPLICATION
    # =========================================================

    controller.show_login()

    sys.exit(
        app.exec()
    )

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
