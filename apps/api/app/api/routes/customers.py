from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import require_permission
from app.core.database import get_db
from app.schemas.customer import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
)
from app.services.customer import CustomerService


router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
)


@router.post(
    "",
    response_model=CustomerResponse,
    status_code=201,
)
def create_customer(
    payload: CustomerCreate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("customer.create")
    ),
):
    return CustomerService.create(
        db,
        payload,
    )


@router.get(
    "",
    response_model=list[CustomerResponse],
)
def list_customers(
    store_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("customer.view")
    ),
):
    return CustomerService.list(
        db,
        store_id,
    )


@router.get(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def get_customer(
    customer_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("customer.view")
    ),
):
    return CustomerService.get(
        db,
        customer_id,
    )


@router.patch(
    "/{customer_id}",
    response_model=CustomerResponse,
)
def update_customer(
    customer_id: UUID,
    payload: CustomerUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(
        require_permission("customer.update")
    ),
):
    return CustomerService.update(
        db,
        customer_id,
        payload,
    )
