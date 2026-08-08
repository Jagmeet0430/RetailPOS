from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_username(
        db: Session,
        username: str,
    ) -> User | None:

        return db.scalar(
            select(User).where(
                User.username == username
            )
        )

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ) -> User | None:

        return db.scalar(
            select(User).where(
                User.email == email
            )
        )

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: UUID,
    ) -> User | None:

        return db.scalar(
            select(User).where(
                User.id == user_id
            )
        )

    @staticmethod
    def create(
        db: Session,
        user: User,
    ) -> User:

        db.add(user)
        db.flush()
        db.refresh(user)

        return user