from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.store import (
    StoreCreate,
    StoreResponse,
)
from app.services.store import StoreService


router = APIRouter(
    prefix="/stores",
    tags=["Stores"],
)


@router.post(
    "",
    response_model=StoreResponse,
    status_code=201,
)
def create_store(
    payload: StoreCreate,
    db: Session = Depends(get_db),
):
    return StoreService.create_store(
        db,
        payload,
    )


@router.get(
    "",
    response_model=list[StoreResponse],
)
def list_stores(
    db: Session = Depends(get_db),
):
    return StoreService.list_stores(db)