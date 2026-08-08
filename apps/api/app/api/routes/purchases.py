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
from app.repositories.purchase import (
    PurchaseRepository,
)
from app.schemas.purchase import (
    PurchaseCreate,
    PurchaseResponse,
)
from app.services.purchase import (
    PurchaseService,
)


router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"],
)


@router.post(
    "",
    response_model=PurchaseResponse,
    status_code=201,
)
def create_purchase(
    payload: PurchaseCreate,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "purchase.create"
        )
    ),
):
    return (
        PurchaseService
        .create_purchase_transaction(
            db,

            store_id=(
                current_user.store_id
            ),

            user_id=(
                current_user.id
            ),

            data=payload,
        )
    )


@router.get(
    "",
    response_model=list[PurchaseResponse],
)
def list_purchases(
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
        require_permission(
            "purchase.view"
        )
    ),
):
    return PurchaseRepository.list(
        db,
        current_user.store_id,
        offset,
        limit,
    )


@router.get(
    "/{purchase_id}",
    response_model=PurchaseResponse,
)
def get_purchase(
    purchase_id: UUID,

    db: Session = Depends(get_db),

    current_user=Depends(
        require_permission(
            "purchase.view"
        )
    ),
):

    purchase = (
        PurchaseRepository.get_by_id(
            db,
            purchase_id,
        )
    )

    if not purchase:
        raise HTTPException(
            status_code=404,
            detail="Purchase not found",
        )

    if (
        purchase.store_id
        != current_user.store_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Access denied",
        )

    return purchase
