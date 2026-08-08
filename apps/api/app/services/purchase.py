from decimal import Decimal
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.purchase import (
    Purchase,
    PurchaseItem,
)
from app.models.supplier import Supplier
from app.repositories.purchase import (
    PurchaseRepository,
)
from app.schemas.purchase import PurchaseCreate
from app.services.inventory import InventoryService
from app.utils.document_numbers import (
    generate_purchase_number,
)


class PurchaseService:

    @staticmethod
    def create_purchase(
        db: Session,
        *,
        store_id: UUID,
        user_id: UUID,
        data: PurchaseCreate,
    ):

        supplier = db.get(
            Supplier,
            data.supplier_id,
        )

        if not supplier:
            raise HTTPException(
                status_code=404,
                detail="Supplier not found",
            )

        if supplier.store_id != store_id:
            raise HTTPException(
                status_code=403,
                detail="Supplier does not belong to this store",
            )

        subtotal = Decimal("0.00")
        discount_total = Decimal("0.00")
        tax_total = Decimal("0.00")

        calculated_items = []

        for item in data.items:

            product = db.get(
                Product,
                item.product_id,
            )

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Product {item.product_id} "
                        "not found"
                    ),
                )

            if product.store_id != store_id:
                raise HTTPException(
                    status_code=403,
                    detail="Product belongs to another store",
                )

            base_amount = (
                item.quantity
                * item.cost_price
            )

            line_total = (
                base_amount
                - item.discount_amount
                + item.tax_amount
            )

            if line_total < 0:
                raise HTTPException(
                    status_code=400,
                    detail="Purchase line total cannot be negative",
                )

            subtotal += base_amount
            discount_total += item.discount_amount
            tax_total += item.tax_amount

            calculated_items.append(
                {
                    "data": item,
                    "line_total": line_total,
                }
            )

        total = (
            subtotal
            - discount_total
            + tax_total
        )

        purchase = Purchase(
            store_id=store_id,
            supplier_id=data.supplier_id,
            user_id=user_id,

            purchase_number=(
                generate_purchase_number()
            ),

            supplier_invoice_number=(
                data.supplier_invoice_number
            ),

            status="completed",

            subtotal=subtotal,
            discount_total=discount_total,
            tax_total=tax_total,
            total=total,

            amount_paid=Decimal("0.00"),

            notes=data.notes,
        )

        db.add(purchase)
        db.flush()

        for calculated in calculated_items:

            item = calculated["data"]

            purchase_item = PurchaseItem(
                purchase_id=purchase.id,
                product_id=item.product_id,

                quantity=item.quantity,
                cost_price=item.cost_price,

                discount_amount=(
                    item.discount_amount
                ),

                tax_amount=item.tax_amount,

                line_total=(
                    calculated["line_total"]
                ),
            )

            db.add(purchase_item)

            InventoryService.change_stock(
                db,
                store_id=store_id,
                product_id=item.product_id,

                quantity_change=(
                    item.quantity
                ),

                movement_type="purchase",

                reference_type="purchase",
                reference_id=purchase.id,

                reason=(
                    f"Purchase "
                    f"{purchase.purchase_number}"
                ),
            )

            product = db.get(
                Product,
                item.product_id,
            )

            product.cost_price = (
                item.cost_price
            )

        db.flush()

        return purchase

    @staticmethod
    def create_purchase_transaction(
        db: Session,
        *,
        store_id: UUID,
        user_id: UUID,
        data: PurchaseCreate,
    ):

        try:
            purchase = (
                PurchaseService.create_purchase(
                    db,
                    store_id=store_id,
                    user_id=user_id,
                    data=data,
                )
            )

            db.commit()
            db.refresh(purchase)

            return (
                PurchaseRepository.get_by_id(
                    db,
                    purchase.id,
                )
            )

        except Exception:
            db.rollback()
            raise
