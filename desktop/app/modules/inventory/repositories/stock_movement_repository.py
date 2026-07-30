from uuid import UUID

from sqlmodel import Session, select

from app.modules.inventory.models.stock_movement import StockMovement


class StockMovementRepository:

    def __init__(self, session: Session):
        self._session = session

    def create(
        self,
        movement: StockMovement,
    ) -> StockMovement:

        self._session.add(movement)
        self._session.flush()

        return movement

    def update(
        self,
        movement: StockMovement,
    ) -> StockMovement:

        self._session.add(movement)
        self._session.commit()
        self._session.refresh(movement)

        return movement

    def delete(
        self,
        movement: StockMovement,
    ) -> None:

        self._session.delete(movement)
        self._session.commit()

    def get_by_id(
        self,
        movement_id: UUID,
    ) -> StockMovement | None:

        return self._session.get(
            StockMovement,
            movement_id,
        )

    def get_all(self) -> list[StockMovement]:

        statement = select(StockMovement)

        return list(
            self._session.exec(statement)
        )

    def get_by_variant(
        self,
        variant_id: UUID,
    ) -> list[StockMovement]:

        statement = (
            select(StockMovement)
            .where(
                StockMovement.variant_id == variant_id
            )
        )

        return list(
            self._session.exec(statement)
        )
    
    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
   