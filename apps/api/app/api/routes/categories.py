from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_permission
from app.core.database import get_db
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.services.category import CategoryService


router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


@router.post(
    "",
    response_model=CategoryResponse,
    status_code=201,
)
def create_category(
    payload: CategoryCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.create")
    ),
):
    return CategoryService.create(db, payload)


@router.get(
    "",
    response_model=list[CategoryResponse],
)
def list_categories(
    store_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.view")
    ),
):
    return CategoryService.list(
        db,
        store_id,
    )


@router.patch(
    "/{category_id}",
    response_model=CategoryResponse,
)
def update_category(
    category_id: UUID,
    payload: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.update")
    ),
):
    return CategoryService.update(
        db,
        category_id,
        payload,
    )
