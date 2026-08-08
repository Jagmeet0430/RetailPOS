from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tax import Tax
from app.schemas.tax import TaxCreate


class TaxRepository:

    @staticmethod
    def list(db: Session):
        return list(
            db.scalars(
                select(Tax)
                .order_by(Tax.rate)
            ).all()
        )

    @staticmethod
    def create(
        db: Session,
        data: TaxCreate,
    ):
        tax = Tax(
            **data.model_dump(),
            is_active=True,
        )

        db.add(tax)
        db.flush()
        db.refresh(tax)

        return tax
