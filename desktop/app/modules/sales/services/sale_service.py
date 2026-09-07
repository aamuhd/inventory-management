from datetime import date
from decimal import Decimal
from uuid import UUID

from app.modules.inventory.enums.movement_type import MovementType
from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)
from app.modules.inventory.services.stock_movement_service import (
    StockMovementService,
)

from app.modules.sales.enums.sale_status import SaleStatus
from app.modules.sales.exceptions import (
    DuplicateSaleItemError,
    EmptySaleError,
    InsufficientStockError,
    InvalidInvoiceNumberError,
    InvalidSaleStateError,
    SaleAlreadyExistsError,
    SaleItemNotFoundError,
    SaleNotFoundError,
)
from app.modules.sales.models.sale import Sale
from app.modules.sales.models.sale_item import SaleItem
from app.modules.sales.repositories.sale_item_repository import (
    SaleItemRepository,
)
from app.modules.sales.repositories.sale_repository import (
    SaleRepository,
)
from app.modules.sales.services.customer_service import CustomerService
from app.modules.settings.services.settings_service import (
    SettingsService,
)


class SaleService:

    def __init__(
        self,
        sale_repository: SaleRepository,
        sale_item_repository: SaleItemRepository,
        customer_service: CustomerService,
        product_variant_service: ProductVariantService,
        stock_movement_service: StockMovementService,
        settings_service: SettingsService,
    ) -> None:

        self._sale_repository = sale_repository
        self._sale_item_repository = sale_item_repository
        self._customer_service = customer_service
        self._product_variant_service = (
            product_variant_service
        )
        self._stock_movement_service = (
            stock_movement_service
        )
        self._settings_service = settings_service

    # =========================================================
    # GENERATE INVOICE NUMBER
    # =========================================================

    def generate_invoice_number(self) -> str:
        """
        Generate the next invoice number using the
        invoice prefix configured in Settings.
        """

        settings = self._settings_service.get()

        prefix = settings.invoice_prefix.strip()

        if not prefix:
            raise InvalidInvoiceNumberError(
                "Invoice prefix is required."
            )

        return self._sale_repository.generate_next_invoice_number(
            prefix
        )

    # =========================================================
    # GET SETTINGS
    # =========================================================

    def get_settings(self):
        """
        Return application settings for presentation features
        such as receipt generation.
        """

        return self._settings_service.get()

    # =========================================================
    # CREATE
    # =========================================================

    def create(
        self,
        customer_id: UUID | None,
        sale_date: date,
        notes: str | None = None,
    ) -> Sale:

        if customer_id is not None:

            self._customer_service.get_by_id(
                customer_id,
            )

        invoice_number = (
            self.generate_invoice_number()
        )

        existing = (
            self._sale_repository.get_by_invoice_number(
                invoice_number,
            )
        )

        if existing is not None:
            raise SaleAlreadyExistsError(
                "Generated invoice number already exists."
            )

        sale = Sale(
            customer_id=customer_id,
            invoice_number=invoice_number,
            sale_date=sale_date,
            notes=notes,
            status=SaleStatus.DRAFT,
            total_amount=Decimal("0.00"),
        )

        return self._sale_repository.create(
            sale,
        )

    # =========================================================
    # GET BY ID
    # =========================================================

    def get_by_id(
        self,
        sale_id: UUID,
    ) -> Sale:

        sale = self._sale_repository.get_by_id(
            sale_id,
        )

        if sale is None:
            raise SaleNotFoundError(
                "Sale not found."
            )

        return sale

    # =========================================================
    # GET ALL
    # =========================================================

    def get_all(
        self,
    ) -> list[Sale]:

        return self._sale_repository.get_all()

    # =========================================================
    # DELETE
    # =========================================================

    def delete(
        self,
        sale_id: UUID,
    ) -> None:

        sale = self.get_by_id(
            sale_id,
        )

        if sale.status != SaleStatus.DRAFT:
            raise InvalidSaleStateError(
                "Only draft sales can be deleted."
            )

        self._sale_repository.delete(
            sale,
        )

    # =========================================================
    # ADD ITEM
    # =========================================================

    def add_item(
        self,
        sale_id: UUID,
        variant_id: UUID,
        quantity: int,
        unit_price: Decimal,
    ) -> SaleItem:

        sale = self.get_by_id(
            sale_id,
        )

        if sale.status != SaleStatus.DRAFT:
            raise InvalidSaleStateError(
                "Only draft sales can be modified."
            )

        variant = (
            self._product_variant_service.get_by_id(
                variant_id,
            )
        )

        if quantity > variant.stock_quantity:
            raise InsufficientStockError(
                "Insufficient stock."
            )

        existing = (
            self._sale_item_repository
            .get_by_sale_and_variant(
                sale_id,
                variant_id,
            )
        )

        if existing is not None:
            raise DuplicateSaleItemError(
                "Variant already exists in this sale."
            )

        item = SaleItem(
            sale_id=sale_id,
            product_variant_id=variant_id,
            quantity=quantity,
            unit_price=unit_price,
        )

        item = self._sale_item_repository.create(
            item,
        )

        self._recalculate_total(
            sale_id,
        )

        return item

    # =========================================================
    # UPDATE ITEM
    # =========================================================

    def update_item(
        self,
        item_id: UUID,
        quantity: int,
        unit_price: Decimal,
    ) -> SaleItem:

        item = self.get_item(
            item_id,
        )

        sale = self.get_by_id(
            item.sale_id,
        )

        if sale.status != SaleStatus.DRAFT:
            raise InvalidSaleStateError(
                "Only draft sales can be modified."
            )

        variant = (
            self._product_variant_service.get_by_id(
                item.product_variant_id,
            )
        )

        if quantity > variant.stock_quantity:
            raise InsufficientStockError(
                "Insufficient stock."
            )

        item.quantity = quantity
        item.unit_price = unit_price

        self._sale_item_repository.update(
            item,
        )

        self._recalculate_total(
            sale.id,
        )

        return item

    # =========================================================
    # DELETE ITEM
    # =========================================================

    def delete_item(
        self,
        item_id: UUID,
    ) -> None:

        item = self.get_item(
            item_id,
        )

        sale = self.get_by_id(
            item.sale_id,
        )

        if sale.status != SaleStatus.DRAFT:
            raise InvalidSaleStateError(
                "Only draft sales can be modified."
            )

        self._sale_item_repository.delete(
            item,
        )

        self._recalculate_total(
            sale.id,
        )

    # =========================================================
    # GET ITEM
    # =========================================================

    def get_item(
        self,
        item_id: UUID,
    ) -> SaleItem:

        item = self._sale_item_repository.get_by_id(
            item_id,
        )

        if item is None:
            raise SaleItemNotFoundError(
                "Sale item not found."
            )

        return item

    # =========================================================
    # RECALCULATE TOTAL
    # =========================================================

    def _recalculate_total(
        self,
        sale_id: UUID,
    ) -> None:

        sale = self.get_by_id(
            sale_id,
        )

        items = (
            self._sale_item_repository.get_by_sale(
                sale_id,
            )
        )

        total = Decimal("0.00")

        for item in items:
            total += (
                item.quantity
                * item.unit_price
            )

        sale.total_amount = total

        self._sale_repository.update(
            sale,
        )

    # =========================================================
    # COMPLETE
    # =========================================================

    def complete(
        self,
        sale_id: UUID,
    ) -> None:

        sale = self.get_by_id(
            sale_id,
        )

        if sale.status != SaleStatus.DRAFT:
            raise InvalidSaleStateError(
                "Sale has already been completed."
            )

        items = (
            self._sale_item_repository.get_by_sale(
                sale_id,
            )
        )

        if not items:
            raise EmptySaleError(
                "Sale contains no items."
            )

        #
        # Validate ALL stock before modifying anything.
        #

        for item in items:

            variant = (
                self._product_variant_service.get_by_id(
                    item.product_variant_id,
                )
            )

            if variant.stock_quantity < item.quantity:

                raise InsufficientStockError(
                    f"Insufficient stock for "
                    f"{variant.product.name} "
                    f"({variant.length} yards)."
                )

        try:

            #
            # Update stock and create movements.
            #

            for item in items:

                self._stock_movement_service.record_movement(
                    variant_id=item.product_variant_id,
                    movement_type=MovementType.SALE,
                    quantity=-item.quantity,
                    reference=sale.invoice_number,
                    notes="Sale",
                )

            #
            # Complete the sale.
            #

            sale.status = SaleStatus.COMPLETED

            self._sale_repository.update(
                sale,
            )

            #
            # ONE commit for the whole operation.
            #

            self._stock_movement_service.commit()

        except Exception:

            self._stock_movement_service.rollback()

            raise

    # =========================================================
    # UPDATE SALE
    # =========================================================

    def update(
        self,
        sale_id: UUID,
        customer_id: UUID | None,
        sale_date: date,
        notes: str | None,
    ) -> Sale:

        sale = self.get_by_id(
            sale_id,
        )

        if sale.status != SaleStatus.DRAFT:
            raise InvalidSaleStateError(
                "Only draft sales can be updated."
            )

        if customer_id is not None:

            self._customer_service.get_by_id(
                customer_id,
            )

        sale.sqlmodel_update(
            {
                "customer_id": customer_id,
                "sale_date": sale_date,
                "notes": notes,
            }
        )

        return self._sale_repository.update(
            sale,
        )