from decimal import Decimal
from uuid import UUID

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class SaleReturn(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sale_returns"

    store_id: Mapped[UUID] = mapped_column(
        ForeignKey("stores.id"),
        nullable=False,
        index=True,
    )

    sale_id: Mapped[UUID] = mapped_column(
        ForeignKey("sales.id"),
        nullable=False,
        index=True,
    )

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    return_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    reason: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    refund_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="completed",
        nullable=False,
    )

    items = relationship(
        "SaleReturnItem",
        back_populates="sale_return",
        cascade="all, delete-orphan",
    )


class SaleReturnItem(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sale_return_items"

    sale_return_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "sale_returns.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    sale_item_id: Mapped[UUID] = mapped_column(
        ForeignKey("sale_items.id"),
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
        nullable=False,
    )

    refund_amount: Mapped[Decimal] = mapped_column(
        Numeric(14, 2),
        nullable=False,
    )

    sale_return = relationship(
        "SaleReturn",
        back_populates="items",
    )
    