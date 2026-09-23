from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import InventoryItem
from app.schemas import MealPromptOut

router = APIRouter(prefix="/meals", tags=["meals"])


@router.get("/prompts", response_model=list[MealPromptOut])
def meal_prompts(db: Session = Depends(get_db)) -> list[MealPromptOut]:
    # TODO: send current inventory to Gemini and return real recipes for the iOS app.
    names = [item.name for item in db.scalars(select(InventoryItem)).all()]
    if not names:
        return []
    return [
        MealPromptOut(
            title="Placeholder meal",
            ingredients_used=names[:8],
            instructions="Replace this stub with a Gemini recipe call.",
        )
    ]
