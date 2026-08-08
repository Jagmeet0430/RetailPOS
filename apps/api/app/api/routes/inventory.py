from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import (
    get_current_user,
    require_permission,
)
from app.core.database import get_db
from app.repositories.inventory import (
    InventoryRepository,
)
from app.schemas.inventory import (
    InventoryResponse,
    OpeningStockCreate,
    StockAdjustmentCreate,
    StockMovementResponse,
)
from app.services.inventory import InventoryService


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"],
)


@router.get(
    "",
    response_model=list[InventoryResponse],
)
def list_inventory(
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory.view")
    ),
):
    return InventoryRepository.list_inventory(
        db,
        current_user.store_id,
    )


@router.get(
    "/{product_id}/movements",
    response_model=list[StockMovementResponse],
)
def stock_movements(
    product_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory.view")
    ),
):
    return InventoryRepository.list_movements(
        db,
        current_user.store_id,
        product_id,
    )


@router.post(
    "/opening-stock",
    response_model=InventoryResponse,
)
def opening_stock(
    payload: OpeningStockCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory.adjust")
    ),
):
    return InventoryService.set_opening_stock(
        db,
        store_id=current_user.store_id,
        product_id=payload.product_id,
        quantity=payload.quantity,
        reason=payload.reason,
    )


@router.post(
    "/adjust",
    response_model=InventoryResponse,
)
def adjust_stock(
    payload: StockAdjustmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("inventory.adjust")
    ),
):
    return InventoryService.adjust_stock(
        db,
        store_id=current_user.store_id,
        product_id=payload.product_id,
        quantity_difference=(
            payload.quantity_difference
        ),
        reason=payload.reason,
    )
