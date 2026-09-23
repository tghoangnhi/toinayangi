"""Telegram / push notification adapter.

Fill in `send_grocery_list` when you wire Telegram or APNs.
"""

from app.config import settings
from app.models import GroceryItem


def send_grocery_list(items: list[GroceryItem]) -> None:
    # TODO: format items and POST to Telegram Bot API (or APNs / web push).
    _ = (settings.telegram_bot_token, settings.telegram_chat_id, items)
    return None
