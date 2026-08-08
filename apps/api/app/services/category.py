from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.category import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:

    @staticmethod
    def create(
        db: Session,
        data: CategoryCreate,
    ):
        category = CategoryRepository.create(db, data)
        db.commit()

        return category

    @staticmethod
    def list(
        db: Session,
        store_id: UUID,
    ):
        return CategoryRepository.list(
            db,
            store_id,
        )

    @staticmethod
    def get(
        db: Session,
        category_id: UUID,
    ):
        category = CategoryRepository.get_by_id(
            db,
            category_id,
        )

        if not category:
            raise HTTPException(
                status_code=404,
                detail="Category not found",
            )

        return category

    @staticmethod
    def update(
        db: Session,
        category_id: UUID,
        data: CategoryUpdate,
    ):
        category = CategoryService.get(
            db,
            category_id,
        )

        category = CategoryRepository.update(
            db,
            category,
            data,
        )

        db.commit()

        return category
