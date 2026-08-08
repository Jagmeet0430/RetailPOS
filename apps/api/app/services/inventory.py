from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.repositories.inventory import InventoryRepository


class InventoryService:

    @staticmethod
    def get_or_create_inventory(
        db: Session,
        store_id: UUID,
        product_id: UUID,
    ):
        inventory = InventoryRepository.get_for_update(
            db,
            store_id,
            product_id,
        )

        if inventory:
            return inventory

        return InventoryRepository.create_inventory(
            db,
            store_id,
            product_id,
        )

    @staticmethod
    def change_stock(
        db: Session,
        *,
        store_id: UUID,
        product_id: UUID,
        quantity_change: Decimal,
        movement_type: str,
        reference_type: str | None = None,
        reference_id: UUID | None = None,
        reason: str | None = None,
    ):
        product = db.get(
            Product,
            product_id,
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        if product.store_id != store_id:
            raise HTTPException(
                status_code=400,
                detail="Product does not belong to this store",
            )

        if not product.track_inventory:
            return None

        inventory = (
            InventoryService.get_or_create_inventory(
                db,
                store_id,
                product_id,
            )
        )

        new_quantity = (
            inventory.quantity
            + quantity_change
        )

        if (
            new_quantity < 0
            and not product.allow_negative_stock
        ):
            raise HTTPException(
                status_code=409,
                detail=(
                    f"Insufficient stock for "
                    f"{product.name}"
                ),
            )

        inventory.quantity = new_quantity

        InventoryRepository.create_movement(
            db,
            store_id=store_id,
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity_change,
            reference_type=reference_type,
            reference_id=reference_id,
            reason=reason,
        )

        db.flush()

        return inventory

    @staticmethod
    def set_opening_stock(
        db: Session,
        *,
        store_id: UUID,
        product_id: UUID,
        quantity: Decimal,
        reason: str | None = None,
    ):

        existing_movements = (
            InventoryRepository.list_movements(
                db,
                store_id,
                product_id,
            )
        )

        if existing_movements:
            raise HTTPException(
                status_code=409,
                detail=(
                    "Opening stock already exists "
                    "or stock has already moved"
                ),
            )

        inventory = (
            InventoryService.change_stock(
                db,
                store_id=store_id,
                product_id=product_id,
                quantity_change=quantity,
                movement_type="opening_stock",
                reason=reason,
            )
        )

        db.commit()

        return inventory

    @staticmethod
    def adjust_stock(
        db: Session,
        *,
        store_id: UUID,
        product_id: UUID,
        quantity_difference: Decimal,
        reason: str,
    ):

        if quantity_difference == 0:
            raise HTTPException(
                status_code=400,
                detail="Adjustment cannot be zero",
            )

        movement_type = (
            "adjustment_in"
            if quantity_difference > 0
            else "adjustment_out"
        )

        inventory = (
            InventoryService.change_stock(
                db,
                store_id=store_id,
                product_id=product_id,
                quantity_change=quantity_difference,
                movement_type=movement_type,
                reason=reason,
            )
        )

        db.commit()

        return inventory
