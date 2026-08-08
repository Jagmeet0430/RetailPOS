from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class BarcodeCreate(BaseModel):
    product_id: UUID

    value: str = Field(
        min_length=1,
        max_length=100,
    )

    is_primary: bool = False


class BarcodeResponse(BaseModel):
    id: UUID
    product_id: UUID
    value: str
    is_primary: bool

    model_config = ConfigDict(
        from_attributes=True
    )
