from uuid import UUID

from app.modules.inventory.enums.movement_type import MovementType
from app.modules.inventory.exceptions import (
    InsufficientStockError,
    InvalidMovementQuantityError,
    ProductVariantNotFoundError,
    StockMovementNotFoundError,
)
from app.modules.inventory.models.stock_movement import StockMovement
from app.modules.inventory.repositories.product_variant_repository import ProductVariantRepository
from app.modules.inventory.repositories.stock_movement_repository import (
    StockMovementRepository,
)
from app.modules.inventory.services.product_variant_service import (
    ProductVariantService,
)



class StockMovementService:

    def __init__(
        self,
        movement_repository: StockMovementRepository,
        variant_repository: ProductVariantRepository,
    ) -> None:

        self._movement_repository = movement_repository
        self._variant_repository = variant_repository

    def purchase_stock(
        self,
        variant_id: UUID,
        quantity: int,
        reference: str | None = None,
        notes: str | None = None,
    ) -> StockMovement:

        return self._record_movement(
            variant_id=variant_id,
            movement_type=MovementType.PURCHASE,
            quantity=quantity,
            reference=reference,
            notes=notes,
        )

    def sell_stock(
        self,
        variant_id: UUID,
        quantity: int,
        reference: str | None = None,
        notes: str | None = None,
    ) -> StockMovement:

        return self._record_movement(
            variant_id=variant_id,
            movement_type=MovementType.SALE,
            quantity=-quantity,
            reference=reference,
            notes=notes,
        )

    def adjust_stock(
        self,
        variant_id: UUID,
        quantity: int,
        reference: str | None = None,
        notes: str | None = None,
    ) -> StockMovement:

        return self._record_movement(
            variant_id=variant_id,
            movement_type=MovementType.ADJUSTMENT,
            quantity=quantity,
            reference=reference,
            notes=notes,
        )

    def return_in(
        self,
        variant_id: UUID,
        quantity: int,
        reference: str | None = None,
        notes: str | None = None,
    ) -> StockMovement:

        return self._record_movement(
            variant_id=variant_id,
            movement_type=MovementType.RETURN_IN,
            quantity=quantity,
            reference=reference,
            notes=notes,
        )

    def damage_stock(
        self,
        variant_id: UUID,
        quantity: int,
        reference: str | None = None,
        notes: str | None = None,
    ) -> StockMovement:

        return self._record_movement(
            variant_id=variant_id,
            movement_type=MovementType.DAMAGED,
            quantity=-quantity,
            reference=reference,
            notes=notes,
        )

    def get_by_id(
        self,
        movement_id: UUID,
    ) -> StockMovement:

        movement = self._movement_repository.get_by_id(
            movement_id,
        )

        if movement is None:
            raise StockMovementNotFoundError(
                "Stock movement not found."
            )

        return movement

    def get_all(self) -> list[StockMovement]:

        return self._movement_repository.get_all()

    def get_by_variant(
        self,
        variant_id: UUID,
    ) -> list[StockMovement]:

        return self._movement_repository.get_by_variant(
            variant_id,
        )

    def delete(
        self,
        movement_id: UUID,
    ) -> None:

        movement = self.get_by_id(
            movement_id,
        )

        self._movement_repository.delete(
            movement,
        )

    def _record_movement(
        self,
        variant_id: UUID,
        movement_type: MovementType,
        quantity: int,
        reference: str | None,
        notes: str | None,
    ) -> StockMovement:

        if quantity == 0:
            raise InvalidMovementQuantityError(
                "Quantity cannot be zero."
            )

        variant = self._variant_repository.get_by_id(
            variant_id,
        )

        if variant is None:
            raise ProductVariantNotFoundError(
                "Product variant not found."
            )

        new_stock = variant.stock_quantity + quantity

        if new_stock < 0:
            raise InsufficientStockError(
                "Insufficient stock."
            )

        variant.stock_quantity = new_stock

        movement = StockMovement(
            variant_id=variant.id,
            movement_type=movement_type,
            quantity=quantity,
            reference=reference,
            notes=notes,
        )

        try:

            self._variant_repository.update_stock(
                variant,
            )

            self._movement_repository.create(
                movement,
            )

            self._movement_repository.commit()

        except Exception:

            self._movement_repository.rollback()

            raise

        return movement
    
    def return_to_supplier(
        self,
        variant_id: UUID,
        quantity: int,
        reference: str | None = None,
        notes: str | None = None,
    ) -> StockMovement:

        return self._record_movement(
            variant_id=variant_id,
            movement_type=MovementType.RETURN_TO_SUPPLIER,
            quantity=-quantity,
            reference=reference,
            notes=notes,
        )

    def sale_stock(
        self,
        *,
        variant_id: UUID,
        quantity: int,
        reference: str,
        notes: str | None = None,
    ) -> StockMovement:

        movement = StockMovement(
            variant_id=variant_id,
            movement_type=MovementType.SALE,
            quantity=-quantity,
            reference=reference,
            notes=notes,
        )

        return self._movement_repository.create(
            movement,
        )