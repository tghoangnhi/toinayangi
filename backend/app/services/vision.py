"""Gemini Flash vision adapter.

Fill in `analyze_fridge_image` with your prompt, schema, and client call.
The scan route only depends on returning a VisionResult.
"""

from pathlib import Path

from app.config import settings
from app.schemas import VisionResult


def analyze_fridge_image(image_path: Path) -> VisionResult:
    # TODO: send image_path to Gemini Flash, parse structured JSON into DetectedItem list.
    # Suggested client: google.genai.Client(api_key=settings.gemini_api_key)
    _ = (settings.gemini_api_key, settings.gemini_model, image_path)
    return VisionResult(items=[], raw_json=None)
