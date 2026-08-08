from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_permission
from app.core.database import get_db
from app.schemas.tax import TaxCreate, TaxResponse
from app.services.tax import TaxService


router = APIRouter(
    prefix="/taxes",
    tags=["Taxes"],
)


@router.get(
    "",
    response_model=list[TaxResponse],
)
def list_taxes(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.view")
    ),
):
    return TaxService.list(db)


@router.post(
    "",
    response_model=TaxResponse,
    status_code=201,
)
def create_tax(
    payload: TaxCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("settings.manage")
    ),
):
    return TaxService.create(
        db,
        payload,
    )
