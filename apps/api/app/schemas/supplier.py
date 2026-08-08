from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SupplierCreate(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=150,
    )
    contact_person: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    tax_number: str | None = None


class SupplierResponse(SupplierCreate):
    id: UUID
    store_id: UUID
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )
