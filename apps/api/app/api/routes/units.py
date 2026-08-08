from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_permission
from app.core.database import get_db
from app.schemas.unit import UnitCreate, UnitResponse
from app.services.unit import UnitService


router = APIRouter(
    prefix="/units",
    tags=["Units"],
)


@router.get(
    "",
    response_model=list[UnitResponse],
)
def list_units(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.view")
    ),
):
    return UnitService.list(db)


@router.post(
    "",
    response_model=UnitResponse,
    status_code=201,
)
def create_unit(
    payload: UnitCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("settings.manage")
    ),
):
    return UnitService.create(
        db,
        payload,
    )
