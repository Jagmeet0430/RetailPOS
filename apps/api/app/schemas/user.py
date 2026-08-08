from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserCreate(BaseModel):
    store_id: UUID
    role_id: UUID

    username: str = Field(
        min_length=3,
        max_length=100,
    )

    email: EmailStr | None = None

    full_name: str = Field(
        min_length=1,
        max_length=150,
    )

    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserResponse(BaseModel):
    id: UUID
    store_id: UUID
    role_id: UUID

    username: str
    email: str | None
    full_name: str

    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    