from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tax import Tax
from app.repositories.tax import TaxRepository
from app.schemas.tax import TaxCreate


class TaxService:

    @staticmethod
    def list(db: Session):
        return TaxRepository.list(db)

    @staticmethod
    def create(
        db: Session,
        data: TaxCreate,
    ):
        existing = db.scalar(
            select(Tax).where(
                Tax.name == data.name
            )
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Tax already exists",
            )

        tax = TaxRepository.create(
            db,
            data,
        )

        db.commit()

        return tax
