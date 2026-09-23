from datetime import datetime

from pydantic import BaseModel, Field


class DetectedItem(BaseModel):
    name: str
    quantity: float = 1.0
    unit: str = "pcs"
    category: str | None = None
    expires_at: datetime | None = None


class VisionResult(BaseModel):
    items: list[DetectedItem] = Field(default_factory=list)
    raw_json: str | None = None


class InventoryItemOut(BaseModel):
    id: int
    name: str
    quantity: float
    unit: str
    category: str | None
    expires_at: datetime | None
    last_seen_at: datetime
    scan_id: int | None

    model_config = {"from_attributes": True}


class InventoryItemUpdate(BaseModel):
    name: str | None = None
    quantity: float | None = None
    unit: str | None = None
    category: str | None = None
    expires_at: datetime | None = None


class ScanOut(BaseModel):
    id: int
    image_path: str
    source: str
    status: str
    error: str | None
    created_at: datetime
    items: list[InventoryItemOut] = Field(default_factory=list)

    model_config = {"from_attributes": True}


class GroceryItemOut(BaseModel):
    id: int
    name: str
    quantity: float
    unit: str
    reason: str | None
    sent_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class MealPromptOut(BaseModel):
    title: str
    ingredients_used: list[str]
    instructions: str
