from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TaxCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )

    rate: Decimal = Field(
        ge=0,
        le=100,
    )


class TaxResponse(BaseModel):
    id: UUID
    name: str
    rate: Decimal
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )
