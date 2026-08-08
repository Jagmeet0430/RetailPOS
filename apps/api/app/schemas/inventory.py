from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class OpeningStockCreate(BaseModel):
    product_id: UUID
    quantity: Decimal = Field(gt=0)
    reason: str | None = "Opening stock"


class StockAdjustmentCreate(BaseModel):
    product_id: UUID
    quantity_difference: Decimal
    reason: str


class InventoryResponse(BaseModel):
    id: UUID
    store_id: UUID
    product_id: UUID
    quantity: Decimal

    model_config = ConfigDict(from_attributes=True)


class StockMovementResponse(BaseModel):
    id: UUID
    store_id: UUID
    product_id: UUID

    movement_type: str
    quantity: Decimal

    reference_type: str | None
    reference_id: UUID | None
    reason: str | None

    model_config = ConfigDict(from_attributes=True)