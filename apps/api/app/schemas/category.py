from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategoryCreate(BaseModel):
    store_id: UUID

    name: str = Field(
        min_length=1,
        max_length=120,
    )

    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
    )

    description: str | None = None
    is_active: bool | None = None


class CategoryResponse(BaseModel):
    id: UUID
    store_id: UUID

    name: str
    description: str | None

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )