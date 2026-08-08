from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate


class SupplierRepository:

    @staticmethod
    def create(
        db: Session,
        *,
        store_id: UUID,
        data: SupplierCreate,
    ) -> Supplier:
        supplier = Supplier(
            store_id=store_id,
            **data.model_dump(),
        )

        db.add(supplier)
        db.flush()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def list(
        db: Session,
        store_id: UUID,
    ) -> list[Supplier]:
        return list(
            db.scalars(
                select(Supplier)
                .where(Supplier.store_id == store_id)
                .order_by(Supplier.name)
            ).all()
        )
