from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.jobs.scheduler import build_and_send_grocery_list
from app.models import GroceryItem
from app.schemas import GroceryItemOut

router = APIRouter(prefix="/grocery", tags=["grocery"])


@router.get("/list", response_model=list[GroceryItemOut])
def grocery_list(db: Session = Depends(get_db)) -> list[GroceryItem]:
    return list(db.scalars(select(GroceryItem).order_by(GroceryItem.created_at.desc())).all())


@router.post("/send", response_model=list[GroceryItemOut])
def send_now(db: Session = Depends(get_db)) -> list[GroceryItem]:
    """Manual trigger so you can test Telegram / push without waiting for cron."""
    build_and_send_grocery_list()
    return list(db.scalars(select(GroceryItem).order_by(GroceryItem.created_at.desc())).all())
