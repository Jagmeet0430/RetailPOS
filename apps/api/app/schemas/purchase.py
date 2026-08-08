from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class PurchaseItemCreate(BaseModel):
    product_id: UUID
    quantity: Decimal = Field(gt=0)
    cost_price: Decimal = Field(ge=0)

    discount_amount: Decimal = Field(default=0, ge=0)
    tax_amount: Decimal = Field(default=0, ge=0)


class PurchaseCreate(BaseModel):
    supplier_id: UUID

    supplier_invoice_number: str | None = None
    notes: str | None = None

    items: list[PurchaseItemCreate] = Field(
        min_length=1
    )


class PurchaseItemResponse(BaseModel):
    id: UUID
    product_id: UUID

    quantity: Decimal
    cost_price: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    line_total: Decimal

    model_config = ConfigDict(
        from_attributes=True
    )


class PurchaseResponse(BaseModel):
    id: UUID

    store_id: UUID
    supplier_id: UUID
    user_id: UUID

    purchase_number: str
    supplier_invoice_number: str | None

    status: str

    subtotal: Decimal
    discount_total: Decimal
    tax_total: Decimal
    total: Decimal
    amount_paid: Decimal

    notes: str | None

    items: list[PurchaseItemResponse]

    model_config = ConfigDict(
        from_attributes=True
    )