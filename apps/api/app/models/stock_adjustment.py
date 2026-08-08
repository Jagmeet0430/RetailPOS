from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class StockAdjustment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "stock_adjustments"

    store_id: Mapped[UUID] = mapped_column(
        ForeignKey("stores.id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    adjustment_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    reason: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="completed",
        nullable=False,
    )

    items = relationship(
        "StockAdjustmentItem",
        back_populates="adjustment",
        cascade="all, delete-orphan",
    )


class StockAdjustmentItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "stock_adjustment_items"

    adjustment_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "stock_adjustments.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    product_id: Mapped[UUID] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
        index=True,
    )

    quantity_difference: Mapped[Decimal] = mapped_column(
        Numeric(14, 3),
        nullable=False,
    )

    item_reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    adjustment = relationship(
        "StockAdjustment",
        back_populates="items",
    )