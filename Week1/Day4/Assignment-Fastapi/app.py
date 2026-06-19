from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import json
import os
import uuid
from datetime import date

app = FastAPI(title="SE DailyStandup tracker", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_FILE = "standups.json"


# ── helpers ──────────────────────────────────────────────────────────────────

def read_data() -> list[dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def write_data(data: list[dict]):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ── schemas ───────────────────────────────────────────────────────────────────

class StandupCreate(BaseModel):
    name: str
    did: str
    doing: str
    blockers: str = "None"


class StandupUpdate(BaseModel):
    did: Optional[str] = None
    doing: Optional[str] = None
    blockers: Optional[str] = None
    status: Optional[str] = None   # "active" | "done"


# ── routes ────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Welcome to SE DSU tracker"}


# POST  — create a new standup entry
@app.post("/standup", status_code=201)
def create_standup(payload: StandupCreate):
    data = read_data()
    entry = {
        "id": str(uuid.uuid4())[:8],
        "name": payload.name,
        "did": payload.did,
        "doing": payload.doing,
        "blockers": payload.blockers,
        "date": str(date.today()),
        "status": "active",
    }
    data.append(entry)
    write_data(data)
    return {"message": "Standup created", "entry": entry}


# GET  — all standups; optional query params: date, status, name
@app.get("/standup")
def get_standups(
    date: Optional[str] = Query(None, description="Filter by date YYYY-MM-DD"),
    status: Optional[str] = Query(None, description="Filter by status: active | done"),
    name: Optional[str] = Query(None, description="Filter by member name"),
):
    data = read_data()
    if date:
        data = [d for d in data if d["date"] == date]
    if status:
        data = [d for d in data if d["status"] == status]
    if name:
        data = [d for d in data if d["name"].lower() == name.lower()]
    return {"count": len(data), "standups": data}


# GET  — single member's full history  (URL param)
@app.get("/standup/{name}")
def get_by_name(name: str):
    data = read_data()
    result = [d for d in data if d["name"].lower() == name.lower()]
    if not result:
        raise HTTPException(status_code=404, detail=f"No standups found for '{name}'")
    return {"name": name, "count": len(result), "standups": result}


# PUT  — update an existing standup by id  (URL param)
@app.put("/standup/{id}")
def update_standup(id: str, payload: StandupUpdate):
    data = read_data()
    for entry in data:
        if entry["id"] == id:
            if payload.did is not None:
                entry["did"] = payload.did
            if payload.doing is not None:
                entry["doing"] = payload.doing
            if payload.blockers is not None:
                entry["blockers"] = payload.blockers
            if payload.status is not None:
                entry["status"] = payload.status
            write_data(data)
            return {"message": "Standup updated", "entry": entry}
    raise HTTPException(status_code=404, detail=f"Standup with id '{id}' not found")


# DELETE  — remove a standup by id  (URL param)
@app.delete("/standup/{id}")
def delete_standup(id: str):
    data = read_data()
    filtered = [d for d in data if d["id"] != id]
    if len(filtered) == len(data):
        raise HTTPException(status_code=404, detail=f"Standup with id '{id}' not found")
    write_data(filtered)
    return {"message": f"Standup '{id}' deleted"}


# GET  — team summary for today  (bonus aggregation endpoint)
@app.get("/standup/summary/today")
def today_summary():
    today = str(date.today())
    data = read_data()
    today_data = [d for d in data if d["date"] == today]
    blocked = [d for d in today_data if d["blockers"].lower() != "none"]
    done = [d for d in today_data if d["status"] == "done"]
    return {
        "date": today,
        "total_entries": len(today_data),
        "done": len(done),
        "active": len(today_data) - len(done),
        "members_with_blockers": [d["name"] for d in blocked],
    }
