from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    sku: str = Field(min_length=1, max_length=100)

    category_id: UUID | None = None
    unit_id: UUID
    tax_id: UUID | None = None

    description: str | None = None

    cost_price: Decimal = Field(default=0, ge=0)
    selling_price: Decimal = Field(gt=0)

    minimum_stock: Decimal = Field(default=0, ge=0)

    track_inventory: bool = True
    allow_negative_stock: bool = False


class ProductCreate(ProductBase):
    store_id: UUID


class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    category_id: UUID | None = None
    unit_id: UUID | None = None
    tax_id: UUID | None = None

    description: str | None = None

    cost_price: Decimal | None = Field(
        default=None,
        ge=0,
    )

    selling_price: Decimal | None = Field(
        default=None,
        gt=0,
    )

    minimum_stock: Decimal | None = Field(
        default=None,
        ge=0,
    )

    track_inventory: bool | None = None
    allow_negative_stock: bool | None = None
    is_active: bool | None = None


class ProductResponse(ProductBase):
    id: UUID
    store_id: UUID
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )