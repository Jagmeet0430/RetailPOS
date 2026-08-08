from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class StoreCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=150,
    )

    code: str = Field(
        min_length=1,
        max_length=50,
    )

    phone: str | None = None
    email: str | None = None
    address: str | None = None


class StoreResponse(BaseModel):
    id: UUID
    name: str
    code: str

    phone: str | None
    email: str | None
    address: str | None

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )