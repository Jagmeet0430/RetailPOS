from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_permission
from app.core.database import get_db
from app.schemas.barcode import (
    BarcodeCreate,
    BarcodeResponse,
)
from app.services.barcode import BarcodeService


router = APIRouter(
    prefix="/barcodes",
    tags=["Barcodes"],
)


@router.post(
    "",
    response_model=BarcodeResponse,
    status_code=201,
)
def create_barcode(
    payload: BarcodeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("product.update")
    ),
):
    return BarcodeService.create(
        db,
        payload,
    )
