from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
)


class ProductRepository:

    @staticmethod
    def create(
        db: Session,
        data: ProductCreate,
    ) -> Product:

        product = Product(
            **data.model_dump()
        )

        db.add(product)
        db.flush()
        db.refresh(product)

        return product

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: UUID,
    ) -> Product | None:

        statement = select(Product).where(
            Product.id == product_id
        )

        return db.scalar(statement)

    @staticmethod
    def get_by_sku(
        db: Session,
        sku: str,
    ) -> Product | None:

        statement = select(Product).where(
            Product.sku == sku
        )

        return db.scalar(statement)

    @staticmethod
    def list(
        db: Session,
        offset: int = 0,
        limit: int = 100,
    ) -> list[Product]:

        statement = (
            select(Product)
            .order_by(Product.name)
            .offset(offset)
            .limit(limit)
        )

        return list(
            db.scalars(statement).all()
        )

    @staticmethod
    def update(
        db: Session,
        product: Product,
        data: ProductUpdate,
    ) -> Product:

        update_data = data.model_dump(
            exclude_unset=True
        )

        for field, value in update_data.items():
            setattr(
                product,
                field,
                value,
            )

        db.flush()
        db.refresh(product)

        return product