from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.product import (
    ProductRepository,
)

from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
)


class ProductService:

    @staticmethod
    def create_product(
        db: Session,
        data: ProductCreate,
    ):
        existing = ProductRepository.get_by_sku(
            db,
            data.sku,
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Product SKU already exists",
            )

        product = ProductRepository.create(
            db,
            data,
        )

        db.commit()

        return product

    @staticmethod
    def get_product(
        db: Session,
        product_id: UUID,
    ):
        product = ProductRepository.get_by_id(
            db,
            product_id,
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        return product

    @staticmethod
    def list_products(
        db: Session,
        offset: int,
        limit: int,
    ):
        return ProductRepository.list(
            db,
            offset,
            limit,
        )

    @staticmethod
    def update_product(
        db: Session,
        product_id: UUID,
        data: ProductUpdate,
    ):
        product = ProductService.get_product(
            db,
            product_id,
        )

        product = ProductRepository.update(
            db,
            product,
            data,
        )

        db.commit()

        return product

    @staticmethod
    def deactivate_product(
        db: Session,
        product_id: UUID,
    ):
        product = ProductService.get_product(
            db,
            product_id,
        )

        product.is_active = False

        db.commit()

        return product