from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.unit import Unit
from app.repositories.unit import UnitRepository
from app.schemas.unit import UnitCreate


class UnitService:

    @staticmethod
    def list(db: Session):
        return UnitRepository.list(db)

    @staticmethod
    def create(
        db: Session,
        data: UnitCreate,
    ):
        existing = db.scalar(
            select(Unit).where(
                Unit.symbol == data.symbol
            )
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Unit symbol already exists",
            )

        unit = UnitRepository.create(
            db,
            data,
        )

        db.commit()

        return unit
