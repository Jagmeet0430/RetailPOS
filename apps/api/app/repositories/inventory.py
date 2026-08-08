from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.inventory import Inventory, StockMovement


class InventoryRepository:

    @staticmethod
    def get(
        db: Session,
        store_id: UUID,
        product_id: UUID,
    ) -> Inventory | None:

        return db.scalar(
            select(Inventory).where(
                Inventory.store_id == store_id,
                Inventory.product_id == product_id,
            )
        )

    @staticmethod
    def get_for_update(
        db: Session,
        store_id: UUID,
        product_id: UUID,
    ) -> Inventory | None:

        return db.scalar(
            select(Inventory)
            .where(
                Inventory.store_id == store_id,
                Inventory.product_id == product_id,
            )
            .with_for_update()
        )

    @staticmethod
    def create_inventory(
        db: Session,
        store_id: UUID,
        product_id: UUID,
    ) -> Inventory:

        inventory = Inventory(
            store_id=store_id,
            product_id=product_id,
            quantity=0,
        )

        db.add(inventory)
        db.flush()

        return inventory

    @staticmethod
    def create_movement(
        db: Session,
        *,
        store_id: UUID,
        product_id: UUID,
        movement_type: str,
        quantity,
        reference_type: str | None = None,
        reference_id: UUID | None = None,
        reason: str | None = None,
    ) -> StockMovement:

        movement = StockMovement(
            store_id=store_id,
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity,
            reference_type=reference_type,
            reference_id=reference_id,
            reason=reason,
        )

        db.add(movement)
        db.flush()

        return movement

    @staticmethod
    def list_inventory(
        db: Session,
        store_id: UUID,
    ) -> list[Inventory]:

        return list(
            db.scalars(
                select(Inventory)
                .where(Inventory.store_id == store_id)
            ).all()
        )

    @staticmethod
    def list_movements(
        db: Session,
        store_id: UUID,
        product_id: UUID,
    ) -> list[StockMovement]:

        return list(
            db.scalars(
                select(StockMovement)
                .where(
                    StockMovement.store_id == store_id,
                    StockMovement.product_id == product_id,
                )
                .order_by(
                    StockMovement.created_at.desc()
                )
            ).all()
        )