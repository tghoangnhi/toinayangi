# Toinayangi backend

FastAPI backbone for the local-first fridge pipeline: Pi snapshot → `POST /inventory/scan` → Gemini (stub) → SQLite → iOS / React / daily grocery job.

## Run

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Docs: http://127.0.0.1:8000/docs

## Endpoints

| Method | Path | Role |
| --- | --- | --- |
| `POST` | `/inventory/scan` | Pi Cam posts a JPEG after the reed switch |
| `GET` | `/inventory/items` | Live inventory for the React dashboard |
| `PATCH` | `/inventory/items/{id}` | Manual edits |
| `GET` | `/meals/prompts` | Meal ideas for the SwiftUI app |
| `GET` | `/grocery/list` | Current grocery list |
| `POST` | `/grocery/send` | Fire the Telegram/push job immediately |

## Fill in later

- `app/services/vision.py` — Gemini Flash structured JSON
- `app/services/inventory.py` — upsert / quantity-diff merge
- `app/services/notify.py` — Telegram or APNs
- `app/jobs/scheduler.py` — how the grocery list is built
- `app/routers/meals.py` — real recipe generation
