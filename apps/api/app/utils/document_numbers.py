from datetime import datetime, timezone
from uuid import uuid4


def generate_purchase_number() -> str:
    now = datetime.now(timezone.utc)

    date_part = now.strftime("%Y%m%d")

    random_part = str(uuid4())[:8].upper()

    return f"PUR-{date_part}-{random_part}"