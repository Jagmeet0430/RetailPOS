from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.purchase import Purchase


class PurchaseRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        purchase_id: UUID,
    ) -> Purchase | None:

        statement = (
            select(Purchase)
            .options(
                selectinload(Purchase.items)
            )
            .where(
                Purchase.id == purchase_id
            )
        )

        return db.scalar(statement)

    @staticmethod
    def list(
        db: Session,
        store_id: UUID,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Purchase]:

        statement = (
            select(Purchase)
            .options(
                selectinload(Purchase.items)
            )
            .where(
                Purchase.store_id == store_id
            )
            .order_by(
                Purchase.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        return list(
            db.scalars(statement)
            .unique()
            .all()
        )