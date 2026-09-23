from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import select

from app.config import settings
from app.database import SessionLocal
from app.models import GroceryItem
from app.services.notify import send_grocery_list

scheduler = BackgroundScheduler()


def build_and_send_grocery_list() -> None:
    # TODO: derive grocery items from inventory (low qty, expiry, missing staples).
    db = SessionLocal()
    try:
        pending = db.scalars(select(GroceryItem).where(GroceryItem.sent_at.is_(None))).all()
        if not pending:
            return
        send_grocery_list(list(pending))
        now = datetime.now(timezone.utc)
        for item in pending:
            item.sent_at = now
        db.commit()
    finally:
        db.close()


def start_scheduler() -> None:
    scheduler.add_job(
        build_and_send_grocery_list,
        "cron",
        hour=settings.grocery_cron_hour,
        minute=settings.grocery_cron_minute,
        id="daily_grocery_list",
        replace_existing=True,
    )
    scheduler.start()


def stop_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)
