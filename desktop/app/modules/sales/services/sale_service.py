from datetime import date
from decimal import Decimal
from uuid import UUID

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


class SaleService:

    def __init__(
        self,
        sale_repository: SaleRepository,
        sale_item_repository: SaleItemRepository,
        customer_service: CustomerService,
        product_variant_service: ProductVariantService,
        stock_movement_service: StockMovementService,
    ) -> None:

        self._sale_repository = sale_repository
        self._sale_item_repository = sale_item_repository
        self._customer_service = customer_service
        self._product_variant_service = product_variant_service
        self._stock_movement_service = stock_movement_service

    def create(
        self,
        customer_id: UUID | None,
        invoice_number: str,
        sale_date: date,
        notes: str | None = None,
    ) -> Sale:

        if not invoice_number.strip():
            raise InvalidInvoiceNumberError(
                "Invoice number is required."
            )

        if customer_id is not None:
            self._customer_service.get_by_id(
                customer_id,
            )

        existing = self._sale_repository.get_by_invoice_number(
            invoice_number,
        )

        if existing is not None:
            raise SaleAlreadyExistsError(
                "Invoice number already exists."
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

    def get_all(
        self,
    ) -> list[Sale]:

        return self._sale_repository.get_all()

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

        variant = self._product_variant_service.get_by_id(
            variant_id,
        )

        if quantity > variant.stock_quantity:
            raise InsufficientStockError(
                "Insufficient stock."
            )

        existing = (
            self._sale_item_repository.get_by_sale_and_variant(
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

    def update_item(
        self,
        item_id: UUID,
        quantity: int,
        unit_price: Decimal,
    ) -> SaleItem:

        item = self.get_item(item_id)

        sale = self.get_by_id(
            item.sale_id,
        )

        if sale.status != SaleStatus.DRAFT:
            raise InvalidSaleStateError(
                "Only draft sales can be modified."
            )

        variant = self._product_variant_service.get_by_id(
            item.product_variant_id,
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

    def delete_item(
        self,
        item_id: UUID,
    ) -> None:

        item = self.get_item(item_id)

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

    def _recalculate_total(
        self,
        sale_id: UUID,
    ) -> None:

        sale = self.get_by_id(
            sale_id,
        )

        items = self._sale_item_repository.get_by_sale(
            sale_id,
        )

        total = Decimal("0.00")

        for item in items:
            total += item.quantity * item.unit_price

        sale.total_amount = total

        self._sale_repository.update(
            sale,
        )

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

        items = self._sale_item_repository.get_by_sale(
            sale_id,
        )

        if not items:
            raise EmptySaleError(
                "Sale contains no items."
            )

        #
        # Validate stock first
        #
        for item in items:

            variant = self._product_variant_service.get_by_id(
                item.product_variant_id,
            )

            if variant.stock_quantity < item.quantity:
                raise InsufficientStockError(
                    f"Insufficient stock for "
                    f"{variant.product.name} ({variant.length} yards)."
                )

        #
        # Deduct stock
        #
        for item in items:

            variant = self._product_variant_service.get_by_id(
                item.product_variant_id,
            )

            variant.stock_quantity -= item.quantity

            self._product_variant_service.update(
                variant_id=variant.id,
                product_id=variant.product_id,
                length=variant.length,
                stock_quantity=variant.stock_quantity,
                reorder_level=variant.reorder_level,
                cost_price=variant.cost_price,
                selling_price=variant.selling_price,
                barcode=variant.barcode,
                sku=variant.sku,
            )

            self._stock_movement_service.sale_stock(
                variant_id=variant.id,
                quantity=item.quantity,
                reference=sale.invoice_number,
                notes="Sale",
            )

        sale.status = SaleStatus.COMPLETED
        print("Sale object:", sale)
        print("Sale ID:", sale.id)
        print("Sale status:", sale.status)
        print("Sale items loaded:", sale.items)
        print("Number of sale items:", len(sale.items))
        self._sale_repository.update(
            sale,
        )

    def update(
        self,
        sale_id: UUID,
        customer_id: UUID | None,
        invoice_number: str,
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
                "invoice_number": invoice_number,
                "sale_date": sale_date,
                "notes": notes,
            }
        )

        return self._sale_repository.update(
            sale,
        )