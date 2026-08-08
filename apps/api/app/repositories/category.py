from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:

    @staticmethod
    def create(db: Session, data: CategoryCreate) -> Category:
        category = Category(**data.model_dump())

        db.add(category)
        db.flush()
        db.refresh(category)

        return category

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: UUID,
    ) -> Category | None:

        return db.scalar(
            select(Category).where(
                Category.id == category_id
            )
        )

    @staticmethod
    def list(
        db: Session,
        store_id: UUID,
    ) -> list[Category]:

        return list(
            db.scalars(
                select(Category)
                .where(Category.store_id == store_id)
                .order_by(Category.name)
            ).all()
        )

    @staticmethod
    def update(
        db: Session,
        category: Category,
        data: CategoryUpdate,
    ) -> Category:

        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(category, field, value)

        db.flush()
        db.refresh(category)

        return category
