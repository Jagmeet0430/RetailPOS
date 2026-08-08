from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_permission
from app.core.database import get_db
from app.schemas.supplier import (
    SupplierCreate,
    SupplierResponse,
)
from app.services.supplier import SupplierService


router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"],
)


@router.post(
    "",
    response_model=SupplierResponse,
    status_code=201,
)
def create_supplier(
    payload: SupplierCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("supplier.create")
    ),
):
    return SupplierService.create(
        db,
        store_id=current_user.store_id,
        data=payload,
    )


@router.get(
    "",
    response_model=list[SupplierResponse],
)
def list_suppliers(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("supplier.view")
    ),
):
    return SupplierService.list(
        db,
        current_user.store_id,
    )
