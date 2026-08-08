from uuid import UUID

from fastapi import (
    Depends,
    HTTPException,
    status,
)

from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user import UserRepository


bearer_scheme = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:

    user_id = decode_access_token(
        credentials.credentials
    )

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    try:
        parsed_user_id = UUID(user_id)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
        )

    user = UserRepository.get_by_id(
        db,
        parsed_user_id,
    )

    if not user or not user.is_active:
        raise HTTPException(
            status_code=401,
            detail="User not available",
        )

    return user


def require_permission(
    permission_code: str,
):

    def permission_dependency(
        current_user: User = Depends(
            get_current_user
        ),
    ):

        role = current_user.role

        if not role:
            raise HTTPException(
                status_code=403,
                detail="No role assigned",
            )

        permission_codes = {
            permission.code
            for permission in role.permissions
        }

        if permission_code not in permission_codes:
            raise HTTPException(
                status_code=403,
                detail="Permission denied",
            )

        return current_user

    return permission_dependency
