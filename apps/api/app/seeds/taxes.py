from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.tax import Tax


DEFAULT_TAXES = [
    {"name": "GST 0%", "rate": Decimal("0.00")},
    {"name": "GST 5%", "rate": Decimal("5.00")},
    {"name": "GST 12%", "rate": Decimal("12.00")},
    {"name": "GST 18%", "rate": Decimal("18.00")},
    {"name": "GST 28%", "rate": Decimal("28.00")},
]


def seed_taxes(db: Session) -> None:
    for data in DEFAULT_TAXES:
        existing = db.scalar(
            select(Tax).where(
                Tax.name == data["name"]
            )
        )

        if existing:
            continue

        db.add(
            Tax(
                name=data["name"],
                rate=data["rate"],
                is_active=True,
            )
        )

    db.flush()