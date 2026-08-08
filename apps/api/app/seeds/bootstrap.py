from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.seeds.permissions import seed_permissions
from app.seeds.roles import seed_roles
from app.seeds.taxes import seed_taxes
from app.seeds.units import seed_units


def bootstrap_database(db: Session) -> None:
    seed_permissions(db)
    seed_roles(db)
    seed_units(db)
    seed_taxes(db)

    db.commit()


def main():
    db = SessionLocal()

    try:
        bootstrap_database(db)
        print("Database seed completed successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()