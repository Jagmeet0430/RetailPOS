from decimal import Decimal
from uuid import UUID

from sqlalchemy import Boolean, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Product(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "products"

    store_id: Mapped[UUID] = mapped_column(
        ForeignKey("stores.id"),
        nullable=False,
        index=True,
    )

    category_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("categories.id"),
        nullable=True,
        index=True,
    )

    unit_id: Mapped[UUID] = mapped_column(
        ForeignKey("units.id"),
        nullable=False,
    )

    tax_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("taxes.id"),
        nullable=True,
    )

    name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    sku: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    cost_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=0,
        nullable=False,
    )

    selling_price: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    minimum_stock: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        default=0,
        nullable=False,
    )

    track_inventory: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    allow_negative_stock: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    store = relationship(
        "Store",
        back_populates="products",
    )

    category = relationship(
        "Category",
        back_populates="products",
    )

    unit = relationship(
        "Unit",
        back_populates="products",
    )

    tax = relationship(
        "Tax",
        back_populates="products",
    )

    barcodes = relationship(
        "Barcode",
        back_populates="product",
        cascade="all, delete-orphan",
    )