from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CustomerCreate(BaseModel):
    store_id: UUID

    name: str = Field(
        min_length=1,
        max_length=150,
    )

    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    tax_number: str | None = None

    credit_limit: Decimal = Field(
        default=0,
        ge=0,
    )


class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: EmailStr | None = None
    address: str | None = None
    tax_number: str | None = None
    credit_limit: Decimal | None = None
    is_active: bool | None = None


class CustomerResponse(CustomerCreate):
    id: UUID
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )
