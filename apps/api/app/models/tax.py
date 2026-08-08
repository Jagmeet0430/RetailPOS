from decimal import Decimal

from sqlalchemy import Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDMixin


class Tax(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "taxes"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    products = relationship(
        "Product",
        back_populates="tax",
    )