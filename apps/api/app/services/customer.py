from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:

    @staticmethod
    def create(
        db: Session,
        data: CustomerCreate,
    ):
        customer = CustomerRepository.create(
            db,
            data,
        )

        db.commit()

        return customer

    @staticmethod
    def list(
        db: Session,
        store_id: UUID,
    ):
        return CustomerRepository.list(
            db,
            store_id,
        )

    @staticmethod
    def get(
        db: Session,
        customer_id: UUID,
    ):
        customer = CustomerRepository.get(
            db,
            customer_id,
        )

        if not customer:
            raise HTTPException(
                status_code=404,
                detail="Customer not found",
            )

        return customer

    @staticmethod
    def update(
        db: Session,
        customer_id: UUID,
        data: CustomerUpdate,
    ):
        customer = CustomerService.get(
            db,
            customer_id,
        )

        customer = CustomerRepository.update(
            db,
            customer,
            data,
        )

        db.commit()

        return customer
