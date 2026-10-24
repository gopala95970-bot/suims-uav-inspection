from datetime import datetime, timezone
from backend.database import insert

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def log_event(level, source, event, detail, mission_id=None):
    return insert("events", {
        "timestamp": now_iso(),
        "level": level,
        "source": source,
        "event": event,
        "detail": detail,
        "mission_id": mission_id
    })
