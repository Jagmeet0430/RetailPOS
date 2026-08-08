from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import (
    CustomerCreate,
    CustomerUpdate,
)


class CustomerRepository:

    @staticmethod
    def create(
        db: Session,
        data: CustomerCreate,
    ):
        customer = Customer(
            **data.model_dump()
        )

        db.add(customer)
        db.flush()
        db.refresh(customer)

        return customer

    @staticmethod
    def get(
        db: Session,
        customer_id: UUID,
    ):
        return db.get(
            Customer,
            customer_id,
        )

    @staticmethod
    def list(
        db: Session,
        store_id: UUID,
    ):
        return list(
            db.scalars(
                select(Customer)
                .where(
                    Customer.store_id == store_id
                )
                .order_by(Customer.name)
            ).all()
        )

    @staticmethod
    def update(
        db: Session,
        customer: Customer,
        data: CustomerUpdate,
    ):
        for field, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(customer, field, value)

        db.flush()
        db.refresh(customer)

        return customer
