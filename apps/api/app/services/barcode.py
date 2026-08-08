from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.barcode import Barcode
from app.models.product import Product
from app.schemas.barcode import BarcodeCreate


class BarcodeService:

    @staticmethod
    def create(
        db: Session,
        data: BarcodeCreate,
    ):
        product = db.get(
            Product,
            data.product_id,
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        duplicate = db.scalar(
            select(Barcode).where(
                Barcode.value == data.value
            )
        )

        if duplicate:
            raise HTTPException(
                status_code=409,
                detail="Barcode already exists",
            )

        if data.is_primary:
            existing_primary = list(
                db.scalars(
                    select(Barcode).where(
                        Barcode.product_id
                        == data.product_id,
                        Barcode.is_primary.is_(True),
                    )
                ).all()
            )

            for barcode in existing_primary:
                barcode.is_primary = False

        barcode = Barcode(
            **data.model_dump()
        )

        db.add(barcode)
        db.commit()
        db.refresh(barcode)

        return barcode
