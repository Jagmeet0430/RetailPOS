from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permission import Permission
from app.models.role import Role


ROLE_PERMISSIONS = {
    "Owner": "*",

    "Manager": [
        "dashboard.view",
        "sale.create",
        "sale.view",
        "sale.refund",
        "sale.discount",
        "product.create",
        "product.view",
        "product.update",
        "inventory.view",
        "inventory.adjust",
        "customer.create",
        "customer.view",
        "customer.update",
        "supplier.create",
        "supplier.view",
        "supplier.update",
        "purchase.create",
        "purchase.view",
        "report.view",
        "cash_register.open",
        "cash_register.close",
    ],

    "Cashier": [
        "dashboard.view",
        "sale.create",
        "sale.view",
        "product.view",
        "customer.create",
        "customer.view",
        "cash_register.open",
        "cash_register.close",
    ],

    "Inventory Manager": [
        "dashboard.view",
        "product.create",
        "product.view",
        "product.update",
        "inventory.view",
        "inventory.adjust",
        "supplier.create",
        "supplier.view",
        "supplier.update",
        "purchase.create",
        "purchase.view",
    ],
}


def seed_roles(db: Session) -> None:
    all_permissions = list(
        db.scalars(
            select(Permission)
        ).all()
    )

    permission_map = {
        permission.code: permission
        for permission in all_permissions
    }

    for role_name, permissions in ROLE_PERMISSIONS.items():
        role = db.scalar(
            select(Role).where(
                Role.name == role_name
            )
        )

        if not role:
            role = Role(
                name=role_name,
                description=f"{role_name} role",
                is_system=True,
            )
            db.add(role)
            db.flush()

        if permissions == "*":
            role.permissions = all_permissions
        else:
            role.permissions = [
                permission_map[code]
                for code in permissions
                if code in permission_map
            ]

    db.flush()