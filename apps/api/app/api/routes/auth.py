from fastapi import (
    APIRouter,
    Depends,
)

from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
    require_permission,
)
from app.core.database import get_db

from app.models.user import User

from app.schemas.user import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)

from app.services.auth import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=201,
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("user.manage")
    ),
):
    return AuthService.create_user(
        db,
        payload,
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    return AuthService.login(
        db,
        payload,
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(
        get_current_user
    ),
):
    return current_user
