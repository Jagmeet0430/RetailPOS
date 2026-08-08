from uuid import UUID

from sqlalchemy.orm import Session

from app.repositories.supplier import SupplierRepository
from app.schemas.supplier import SupplierCreate


class SupplierService:

    @staticmethod
    def create(
        db: Session,
        *,
        store_id: UUID,
        data: SupplierCreate,
    ):
        supplier = SupplierRepository.create(
            db,
            store_id=store_id,
            data=data,
        )

        db.commit()

        return supplier

    @staticmethod
    def list(
        db: Session,
        store_id: UUID,
    ):
        return SupplierRepository.list(
            db,
            store_id,
        )
