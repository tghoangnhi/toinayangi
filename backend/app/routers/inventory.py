from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import InventoryItem, Scan
from app.schemas import InventoryItemOut, InventoryItemUpdate, ScanOut
from app.services.inventory import apply_scan_to_inventory
from app.services.vision import analyze_fridge_image

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.post("/scan", response_model=ScanOut)
async def scan_inventory(
    image: UploadFile = File(...),
    source: str = Form("pi-cam"),
    db: Session = Depends(get_db),
) -> Scan:
    """Pi posts a snapshot here after the reed switch fires."""
    upload_root = Path(settings.upload_dir)
    upload_root.mkdir(parents=True, exist_ok=True)
    suffix = Path(image.filename or "frame.jpg").suffix or ".jpg"
    dest = upload_root / f"{uuid4().hex}{suffix}"
    dest.write_bytes(await image.read())

    scan = Scan(image_path=str(dest), source=source, status="processing")
    db.add(scan)
    db.commit()
    db.refresh(scan)

    try:
        vision = analyze_fridge_image(dest)
        scan.raw_vision_json = vision.raw_json
        apply_scan_to_inventory(db, scan, vision)
        scan.status = "complete"
        db.commit()
        db.refresh(scan)
    except Exception as exc:
        scan.status = "failed"
        scan.error = str(exc)
        db.commit()
        db.refresh(scan)

    return scan


@router.get("/scans", response_model=list[ScanOut])
def list_scans(db: Session = Depends(get_db)) -> list[Scan]:
    return list(db.scalars(select(Scan).order_by(Scan.created_at.desc())).all())


@router.get("/items", response_model=list[InventoryItemOut])
def list_items(db: Session = Depends(get_db)) -> list[InventoryItem]:
    return list(db.scalars(select(InventoryItem).order_by(InventoryItem.name)).all())


@router.patch("/items/{item_id}", response_model=InventoryItemOut)
def update_item(item_id: int, payload: InventoryItemUpdate, db: Session = Depends(get_db)) -> InventoryItem:
    item = db.get(InventoryItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    item = db.get(InventoryItem, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
