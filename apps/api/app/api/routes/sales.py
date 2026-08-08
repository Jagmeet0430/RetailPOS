from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy.orm import Session

from app.api.dependencies import (
    require_permission,
)
from app.core.database import get_db
from app.repositories.sale import SaleRepository
from app.schemas.sale import (
    SaleCreate,
    SaleResponse,
)
from app.services.sale import SaleService


router = APIRouter(
    prefix="/sales",
    tags=["Sales"],
)


@router.post(
    "",
    response_model=SaleResponse,
    status_code=201,
)
def checkout(
    payload: SaleCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission("sale.create")
    ),
):
    return SaleService.checkout(
        db,
        store_id=current_user.store_id,
        cashier_id=current_user.id,
        data=payload,
    )


@router.get(
    "",
    response_model=list[SaleResponse],
)
def list_sales(
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
        require_permission("sale.view")
    ),
):
    return SaleRepository.list(
        db,
        current_user.store_id,
        offset,
        limit,
    )


@router.get(
    "/{sale_id}",
    response_model=SaleResponse,
)
def get_sale(
    sale_id: UUID,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission("sale.view")
    ),
):

    sale = SaleRepository.get_by_id(
        db,
        sale_id,
    )

    if not sale:
        raise HTTPException(
            status_code=404,
            detail="Sale not found",
        )

    if (
        sale.store_id
        != current_user.store_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    return sale