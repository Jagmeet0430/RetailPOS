from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.store import StoreRepository
from app.schemas.store import StoreCreate


class StoreService:

    @staticmethod
    def create_store(
        db: Session,
        data: StoreCreate,
    ):

        existing = StoreRepository.get_by_code(
            db,
            data.code,
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Store code already exists",
            )

        store = StoreRepository.create(
            db,
            data,
        )

        db.commit()

        return store

    @staticmethod
    def list_stores(
        db: Session,
    ):

        return StoreRepository.list(db)