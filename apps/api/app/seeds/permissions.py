from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission import Permission


DEFAULT_PERMISSIONS = [
    ("dashboard.view", "View dashboard"),

    ("sale.create", "Create sales"),
    ("sale.view", "View sales"),
    ("sale.refund", "Refund sales"),
    ("sale.discount", "Apply discounts"),

    ("product.create", "Create products"),
    ("product.view", "View products"),
    ("product.update", "Update products"),
    ("product.delete", "Deactivate products"),

    ("inventory.view", "View inventory"),
    ("inventory.adjust", "Adjust inventory"),

    ("customer.create", "Create customers"),
    ("customer.view", "View customers"),
    ("customer.update", "Update customers"),

    ("supplier.create", "Create suppliers"),
    ("supplier.view", "View suppliers"),
    ("supplier.update", "Update suppliers"),

    ("purchase.create", "Create purchases"),
    ("purchase.view", "View purchases"),

    ("report.view", "View reports"),

    ("cash_register.open", "Open cash register"),
    ("cash_register.close", "Close cash register"),

    ("user.manage", "Manage users"),
    ("role.manage", "Manage roles"),

    ("settings.manage", "Manage settings"),
]


def seed_permissions(db: Session) -> None:
    for code, description in DEFAULT_PERMISSIONS:
        existing = db.scalar(
            select(Permission).where(
                Permission.code == code
            )
        )

        if existing:
            continue

        name = code.replace(".", " ").title()

        db.add(
            Permission(
                name=name,
                code=code,
                description=description,
            )
        )

    db.flush()