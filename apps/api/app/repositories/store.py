from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.store import Store
from app.schemas.store import StoreCreate


class StoreRepository:

    @staticmethod
    def create(
        db: Session,
        data: StoreCreate,
    ) -> Store:

        store = Store(
            **data.model_dump()
        )

        db.add(store)
        db.flush()
        db.refresh(store)

        return store

    @staticmethod
    def get_by_code(
        db: Session,
        code: str,
    ) -> Store | None:

        return db.scalar(
            select(Store).where(
                Store.code == code
            )
        )

    @staticmethod
    def list(
        db: Session,
    ) -> list[Store]:

        return list(
            db.scalars(
                select(Store)
                .order_by(Store.name)
            ).all()
        )