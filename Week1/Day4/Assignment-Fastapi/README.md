# Standup — Live Standup Bot

A team standup board built to demo all four HTTP methods (GET, POST, PUT, DELETE) with both URL and query parameters, using FastAPI on the backend and Streamlit on the frontend. Data is stored in a flat JSON file — no database required.

![Status](https://img.shields.io/badge/status-MVP-5B5FEF) ![FastAPI](https://img.shields.io/badge/backend-FastAPI-009688) ![Streamlit](https://img.shields.io/badge/frontend-Streamlit-FF4B4B)

---

## What it does

Each team member posts what they did yesterday, what they're doing today, and any blockers. The board shows everyone's update as a card, filterable by date and status, with live stats at the top (total, completed, in progress, blocked).

---

## Tech stack

| Layer | Tool |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| Storage | `standups.json` (flat file) |
| Validation | Pydantic |
| HTTP client (frontend → backend) | `requests` |

---

## Project structure

```
.
├── app.py              # FastAPI backend
├── frontend.py         # Streamlit UI
├── requirements.txt
├── standups.json        # auto-created on first POST
└── README.md
```

---

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install -r requirements.txt
```

---

## Running the app

Open **two terminals** in the project folder.

**Terminal 1 — backend**
```bash
uvicorn app:app --reload
```
Runs at `http://127.0.0.1:8000`
Interactive API docs (Swagger): `http://127.0.0.1:8000/docs`

**Terminal 2 — frontend**
```bash
streamlit run frontend.py
```
Runs at `http://localhost:8501`

> The frontend depends on the backend being up first — start `app.py` before `frontend.py`.

---

## API reference

| Method | Endpoint | Param type | Purpose |
|---|---|---|---|
| `POST` | `/standup` | Request body | Create a new standup entry |
| `GET` | `/standup` | Query params (`date`, `status`, `name`) | List standups, optionally filtered |
| `GET` | `/standup/{name}` | URL param | Get full history for one person |
| `PUT` | `/standup/{id}` | URL param + body | Update an entry's content or status |
| `DELETE` | `/standup/{id}` | URL param | Remove an entry |
| `GET` | `/standup/summary/today` | — | Aggregated stats for today |

### Example requests

**Create a standup**
```bash
curl -X POST http://127.0.0.1:8000/standup \
  -H "Content-Type: application/json" \
  -d '{"name":"Sudha","did":"Built login page","doing":"Working on API","blockers":"None"}'
```

**Filter by date and status**
```bash
curl "http://127.0.0.1:8000/standup?date=2026-06-19&status=active"
```

**Get one person's history**
```bash
curl http://127.0.0.1:8000/standup/Sudha
```

**Mark as done**
```bash
curl -X PUT http://127.0.0.1:8000/standup/ea10fefd \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}'
```

**Delete an entry**
```bash
curl -X DELETE http://127.0.0.1:8000/standup/ea10fefd
```

---

## Data model

Each entry stored in `standups.json`:

```json
{
  "id": "ea10fefd",
  "name": "Sudha",
  "did": "Built login page",
  "doing": "Working on API",
  "blockers": "None",
  "date": "2026-06-19",
  "status": "active"
}
```

---

## Frontend features

- **Stat tiles** — live count of total, completed, in-progress, and blocked entries for today
- **New standup form** — posts a new card to the board
- **Date + status filters** — query the backend live, no page reload
- **Sticky-note cards** — one per entry, with avatar initials and a status pill
- **Inline actions per card** — Edit (PUT), Done/Undo (PUT), Delete (DELETE)
- **Sidebar member lookup** — search any person's full standup history
- **Glassmorphic UI** — frosted glass cards over a soft gradient background, Inter + JetBrains Mono type system

---

## Testing with Postman

1. Start the backend.
2. In Postman: **Import → Link** → paste `http://127.0.0.1:8000/openapi.json`
3. This generates a full collection with all six endpoints pre-filled.

---

## Notes

- No database setup needed — `standups.json` is created automatically on the first POST.
- CORS is open (`allow_origins=["*"]`) for local demo purposes only; restrict this before any real deployment.
- IDs are short UUIDs (8 characters) for readability during a live demo.
