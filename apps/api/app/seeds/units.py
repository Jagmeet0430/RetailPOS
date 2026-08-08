from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.unit import Unit


DEFAULT_UNITS = [
    {"name": "Piece", "symbol": "pcs"},
    {"name": "Kilogram", "symbol": "kg"},
    {"name": "Gram", "symbol": "g"},
    {"name": "Litre", "symbol": "L"},
    {"name": "Millilitre", "symbol": "ml"},
    {"name": "Box", "symbol": "box"},
    {"name": "Packet", "symbol": "pkt"},
]


def seed_units(db: Session) -> None:
    for data in DEFAULT_UNITS:
        existing = db.scalar(
            select(Unit).where(
                Unit.symbol == data["symbol"]
            )
        )

        if existing:
            continue

        db.add(Unit(**data))

    db.flush()