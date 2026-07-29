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
from app.modules.inventory.repositories.category_repository import CategoryRepository
from app.modules.inventory.repositories.product_repository import ProductRepository
from app.modules.inventory.repositories.product_variant_repository import ProductVariantRepository
from app.modules.inventory.repositories.purchase_order_item_repository import PurchaseOrderItemRepository
from app.modules.inventory.repositories.purchase_order_repository import PurchaseOrderRepository
from app.modules.inventory.repositories.supplier_repository import SupplierRepository
from app.modules.inventory.repositories.supplier_return_item_repository import SupplierReturnItemRepository
from app.modules.inventory.repositories.supplier_return_repository import SupplierReturnRepository
from app.modules.inventory.repositories.stock_movement_repository import StockMovementRepository
from app.modules.inventory.services.category_service import CategoryService
from app.modules.inventory.services.product_service import ProductService
from app.modules.inventory.services.product_variant_service import ProductVariantService
from app.modules.inventory.services.purchase_order_service import PurchaseOrderService
from app.modules.inventory.services.stock_movement_service import StockMovementService
from app.modules.inventory.services.supplier_return_service import SupplierReturnService
from app.modules.inventory.services.supplier_service import SupplierService



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
    category_repository = CategoryRepository(session)
    product_repository = ProductRepository(session)
    variant_repository = ProductVariantRepository(session)
    supplier_repository = SupplierRepository(session)
    purchase_order_repository = PurchaseOrderRepository(session)
    supplier_return_repository = SupplierReturnRepository(session)
    supplier_return_item_repository = SupplierReturnItemRepository(session)
    purchase_order_item_repository = PurchaseOrderItemRepository(session)
    movement_repository = StockMovementRepository(session)

    password_hasher = PasswordHasher()

    authentication_service = AuthenticationService(
        user_repository=user_repository,
        password_hasher=password_hasher,
    )
    category_service = CategoryService(
        repository=category_repository,
    )

    product_service = ProductService(
        product_repository=product_repository,
    )

    product_variant_service = ProductVariantService(
        variant_repository=variant_repository,
        product_service=product_service
    )

    supplier_service = SupplierService(
        repository=supplier_repository,
    )

    stock_movement_service = StockMovementService(
        movement_repository=movement_repository,
        variant_repository=variant_repository
    )

    purchase_order_service = PurchaseOrderService(
        purchase_order_repository=purchase_order_repository,
        purchase_order_item_repository=purchase_order_item_repository,
        supplier_service=supplier_service,
        product_variant_service=product_variant_service,
        stock_movement_service=stock_movement_service
    )

    supplier_return_service = SupplierReturnService(
        return_repository=supplier_return_repository,
        item_repository=supplier_return_item_repository,
        stock_movement_service=stock_movement_service
    )

    current_session = CurrentSession()

    controller = ApplicationController(
        authentication_service=authentication_service,
        current_session=current_session,
        category_service=category_service,
        product_service=product_service,
        variant_service=product_variant_service,
        supplier_service=supplier_service,
        purchase_order_service=purchase_order_service,
        supplier_return_service=supplier_return_service
    )

    controller.show_login()

    sys.exit(app.exec())
        


if __name__ == "__main__":
    main()
    
