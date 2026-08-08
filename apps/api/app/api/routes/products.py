from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
    require_permission,
)
from app.core.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
)
from app.services.product import (
    ProductService,
)


router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.post(
    "",
    response_model=ProductResponse,
    status_code=201,
)
def create_product(
    payload: ProductCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.create")
    ),
):
    return ProductService.create_product(
        db,
        payload,
    )


@router.get(
    "",
    response_model=list[ProductResponse],
)
def list_products(
    offset: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.view")
    ),
):
    return ProductService.list_products(
        db,
        offset,
        limit,
    )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.view")
    ),
):
    return ProductService.get_product(
        db,
        product_id,
    )


@router.patch(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: UUID,
    payload: ProductUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.update")
    ),
):
    return ProductService.update_product(
        db,
        product_id,
        payload,
    )


@router.delete(
    "/{product_id}",
    response_model=ProductResponse,
)
def deactivate_product(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.delete")
    ),
):
    return ProductService.deactivate_product(
        db,
        product_id,
    )
