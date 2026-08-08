from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.unit import Unit
from app.schemas.unit import UnitCreate


class UnitRepository:

    @staticmethod
    def list(db: Session) -> list[Unit]:

        return list(
            db.scalars(
                select(Unit)
                .order_by(Unit.name)
            ).all()
        )

    @staticmethod
    def create(
        db: Session,
        data: UnitCreate,
    ) -> Unit:

        unit = Unit(**data.model_dump())

        db.add(unit)
        db.flush()
        db.refresh(unit)

        return unit
