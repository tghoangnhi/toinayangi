"""Inventory merge helpers.

Replace replace-all-from-scan with your own upsert / quantity-diff logic.
"""

from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import InventoryItem, Scan
from app.schemas import VisionResult


def apply_scan_to_inventory(db: Session, scan: Scan, vision: VisionResult) -> list[InventoryItem]:
    # TODO: merge detected items with existing rows instead of naive insert.
    created: list[InventoryItem] = []
    now = datetime.now(timezone.utc)
    for detected in vision.items:
        item = InventoryItem(
            name=detected.name,
            quantity=detected.quantity,
            unit=detected.unit,
            category=detected.category,
            expires_at=detected.expires_at,
            last_seen_at=now,
            scan_id=scan.id,
        )
        db.add(item)
        created.append(item)
    return created
