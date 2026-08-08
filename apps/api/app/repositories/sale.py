from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.sale import Sale


class SaleRepository:

    @staticmethod
    def get_by_id(
        db: Session,
        sale_id: UUID,
    ) -> Sale | None:

        statement = (
            select(Sale)
            .options(
                selectinload(Sale.items),
                selectinload(Sale.payments),
            )
            .where(Sale.id == sale_id)
        )

        return db.scalar(statement)

    @staticmethod
    def list(
        db: Session,
        store_id: UUID,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Sale]:

        statement = (
            select(Sale)
            .options(
                selectinload(Sale.items),
                selectinload(Sale.payments),
            )
            .where(
                Sale.store_id == store_id
            )
            .order_by(
                Sale.created_at.desc()
            )
            .offset(offset)
            .limit(limit)
        )

        return list(
            db.scalars(statement)
            .unique()
            .all()
        )