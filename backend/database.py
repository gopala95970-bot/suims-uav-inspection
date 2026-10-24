import sqlite3
from pathlib import Path
from .config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS missions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TEXT,
    completed_at TEXT,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    level TEXT NOT NULL,
    source TEXT NOT NULL,
    event TEXT NOT NULL,
    detail TEXT NOT NULL,
    mission_id INTEGER
);

CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    proposed_action TEXT NOT NULL,
    final_action TEXT NOT NULL,
    reason TEXT NOT NULL,
    priority TEXT NOT NULL,
    risk_score REAL NOT NULL,
    mission_id INTEGER
);

CREATE TABLE IF NOT EXISTS detections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT NOT NULL,
    asset_id TEXT NOT NULL,
    defect_type TEXT NOT NULL,
    confidence REAL NOT NULL,
    severity TEXT NOT NULL,
    recurring INTEGER NOT NULL,
    source TEXT NOT NULL,
    risk_score REAL NOT NULL,
    mission_id INTEGER
);
"""

def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA)
    return conn

def insert(table, data):
    conn = connect()
    cols = ", ".join(data.keys())
    marks = ", ".join("?" for _ in data)
    cur = conn.execute(f"INSERT INTO {table} ({cols}) VALUES ({marks})", tuple(data.values()))
    conn.commit()
    row_id = cur.lastrowid
    conn.close()
    return row_id

def fetch_all(query, params=()):
    conn = connect()
    rows = [dict(r) for r in conn.execute(query, params).fetchall()]
    conn.close()
    return rows

def fetch_one(query, params=()):
    conn = connect()
    row = conn.execute(query, params).fetchone()
    conn.close()
    return dict(row) if row else None
