from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SaleItemCreate(BaseModel):
    product_id: UUID
    quantity: Decimal = Field(gt=0)

    discount_amount: Decimal = Field(
        default=0,
        ge=0,
    )


class PaymentCreate(BaseModel):
    payment_method: str = Field(
        min_length=1,
        max_length=30,
    )

    amount: Decimal = Field(
        gt=0,
    )

    reference_number: str | None = None


class SaleCreate(BaseModel):
    customer_id: UUID | None = None
    cash_session_id: UUID | None = None

    items: list[SaleItemCreate] = Field(
        min_length=1
    )

    payments: list[PaymentCreate] = Field(
        min_length=1
    )


class SaleItemResponse(BaseModel):
    id: UUID
    product_id: UUID

    quantity: Decimal
    unit_price: Decimal
    cost_price: Decimal

    discount_amount: Decimal
    tax_amount: Decimal
    line_total: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class PaymentResponse(BaseModel):
    id: UUID

    payment_method: str
    amount: Decimal
    reference_number: str | None

    model_config = ConfigDict(
        from_attributes=True
    )


class SaleResponse(BaseModel):
    id: UUID

    store_id: UUID
    customer_id: UUID | None
    cashier_id: UUID
    cash_session_id: UUID | None

    invoice_number: str
    status: str

    subtotal: Decimal
    discount_total: Decimal
    tax_total: Decimal
    total: Decimal

    amount_paid: Decimal
    change_amount: Decimal

    items: list[SaleItemResponse]
    payments: list[PaymentResponse]

    model_config = ConfigDict(
        from_attributes=True
    )