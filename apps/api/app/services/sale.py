from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.payment import Payment
from app.models.product import Product
from app.models.sale import Sale, SaleItem

from app.repositories.sale import SaleRepository
from app.schemas.sale import SaleCreate
from app.services.inventory import InventoryService
from app.utils.document_numbers import (
    generate_invoice_number,
)


MONEY = Decimal("0.01")


def money(value: Decimal) -> Decimal:
    return value.quantize(
        MONEY,
        rounding=ROUND_HALF_UP,
    )


class SaleService:

    @staticmethod
    def create_sale(
        db: Session,
        *,
        store_id: UUID,
        cashier_id: UUID,
        data: SaleCreate,
    ):

        if data.customer_id:
            customer = db.get(
                Customer,
                data.customer_id,
            )

            if not customer:
                raise HTTPException(
                    status_code=404,
                    detail="Customer not found",
                )

            if customer.store_id != store_id:
                raise HTTPException(
                    status_code=403,
                    detail="Customer belongs to another store",
                )

        subtotal = Decimal("0.00")
        discount_total = Decimal("0.00")
        tax_total = Decimal("0.00")

        calculated_items = []

        for request_item in data.items:

            product = db.get(
                Product,
                request_item.product_id,
            )

            if not product:
                raise HTTPException(
                    status_code=404,
                    detail=(
                        f"Product {request_item.product_id} not found"
                    ),
                )

            if product.store_id != store_id:
                raise HTTPException(
                    status_code=403,
                    detail="Product belongs to another store",
                )

            if not product.is_active:
                raise HTTPException(
                    status_code=409,
                    detail=f"{product.name} is inactive",
                )

            base_amount = money(
                request_item.quantity
                * product.selling_price
            )

            if request_item.discount_amount > base_amount:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Discount exceeds line value for "
                        f"{product.name}"
                    ),
                )

            taxable_amount = (
                base_amount
                - request_item.discount_amount
            )

            tax_amount = Decimal("0.00")

            if product.tax:
                tax_amount = money(
                    taxable_amount
                    * product.tax.rate
                    / Decimal("100")
                )

            line_total = money(
                taxable_amount + tax_amount
            )

            subtotal += base_amount
            discount_total += request_item.discount_amount
            tax_total += tax_amount

            calculated_items.append(
                {
                    "request": request_item,
                    "product": product,
                    "tax_amount": tax_amount,
                    "line_total": line_total,
                }
            )

        subtotal = money(subtotal)
        discount_total = money(discount_total)
        tax_total = money(tax_total)

        total = money(
            subtotal
            - discount_total
            + tax_total
        )

        payment_total = money(
            sum(
                (
                    payment.amount
                    for payment in data.payments
                ),
                Decimal("0.00"),
            )
        )

        if payment_total < total:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Insufficient payment. "
                    f"Required {total}, received {payment_total}"
                ),
            )

        change_amount = money(
            payment_total - total
        )

        sale = Sale(
            store_id=store_id,
            customer_id=data.customer_id,
            cashier_id=cashier_id,
            cash_session_id=data.cash_session_id,

            invoice_number=(
                generate_invoice_number()
            ),

            status="completed",

            subtotal=subtotal,
            discount_total=discount_total,
            tax_total=tax_total,
            total=total,

            amount_paid=payment_total,
            change_amount=change_amount,
        )

        db.add(sale)
        db.flush()

        for calculated in calculated_items:

            request_item = calculated["request"]
            product = calculated["product"]

            sale_item = SaleItem(
                sale_id=sale.id,
                product_id=product.id,

                quantity=request_item.quantity,

                unit_price=product.selling_price,
                cost_price=product.cost_price,

                discount_amount=(
                    request_item.discount_amount
                ),

                tax_amount=(
                    calculated["tax_amount"]
                ),

                line_total=(
                    calculated["line_total"]
                ),
            )

            db.add(sale_item)

            InventoryService.change_stock(
                db,

                store_id=store_id,
                product_id=product.id,

                quantity_change=(
                    -request_item.quantity
                ),

                movement_type="sale",

                reference_type="sale",
                reference_id=sale.id,

                reason=(
                    f"Sale {sale.invoice_number}"
                ),
            )

        for request_payment in data.payments:

            payment = Payment(
                sale_id=sale.id,

                payment_method=(
                    request_payment.payment_method
                ),

                amount=request_payment.amount,

                reference_number=(
                    request_payment.reference_number
                ),
            )

            db.add(payment)

        db.flush()

        return sale

    @staticmethod
    def checkout(
        db: Session,
        *,
        store_id: UUID,
        cashier_id: UUID,
        data: SaleCreate,
    ):

        try:
            sale = SaleService.create_sale(
                db,
                store_id=store_id,
                cashier_id=cashier_id,
                data=data,
            )

            db.commit()

            return SaleRepository.get_by_id(
                db,
                sale.id,
            )

        except Exception:
            db.rollback()
            raise
