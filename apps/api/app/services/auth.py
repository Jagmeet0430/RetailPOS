from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)

from app.models.user import User

from app.repositories.user import UserRepository

from app.schemas.user import (
    LoginRequest,
    UserCreate,
)


class AuthService:

    @staticmethod
    def create_user(
        db: Session,
        data: UserCreate,
    ) -> User:

        existing = UserRepository.get_by_username(
            db,
            data.username,
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Username already exists",
            )

        if data.email:
            existing_email = UserRepository.get_by_email(
                db,
                data.email,
            )

            if existing_email:
                raise HTTPException(
                    status_code=409,
                    detail="Email already exists",
                )

        user = User(
            store_id=data.store_id,
            role_id=data.role_id,
            username=data.username,
            email=data.email,
            full_name=data.full_name,
            password_hash=hash_password(
                data.password
            ),
            is_active=True,
        )

        user = UserRepository.create(
            db,
            user,
        )

        db.commit()

        return user

    @staticmethod
    def login(
        db: Session,
        data: LoginRequest,
    ):

        user = UserRepository.get_by_username(
            db,
            data.username,
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        if not verify_password(
            data.password,
            user.password_hash,
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=403,
                detail="User is inactive",
            )

        token = create_access_token(
            str(user.id)
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }