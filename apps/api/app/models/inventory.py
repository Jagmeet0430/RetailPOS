from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Inventory(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "inventory"

    __table_args__ = (
        UniqueConstraint(
            "store_id",
            "product_id",
            name="uq_inventory_store_product",
        ),
    )

    store_id: Mapped[UUID] = mapped_column(
        ForeignKey("stores.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        default=0,
        nullable=False,
    )


class StockMovement(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "stock_movements"

    store_id: Mapped[UUID] = mapped_column(
        ForeignKey("stores.id"),
        nullable=False,
        index=True,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    movement_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        index=True,
    )

    quantity: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )

    reference_type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    reference_id: Mapped[UUID | None] = mapped_column(
        nullable=True,
    )

    reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
