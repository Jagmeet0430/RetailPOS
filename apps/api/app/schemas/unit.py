from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UnitCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=50,
    )

    symbol: str = Field(
        min_length=1,
        max_length=20,
    )


class UnitResponse(BaseModel):
    id: UUID
    name: str
    symbol: str

    model_config = ConfigDict(
        from_attributes=True
    )
