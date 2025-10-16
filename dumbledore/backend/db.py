# backend/db.py
import sqlite3
from datetime import datetime
DB = "magic_spells.db"


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attempts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT,
        ts TEXT,
        raw TEXT,
        normalized TEXT,
        recognized INTEGER,
        spell TEXT,
        score REAL
    )
    """)
    con.commit()
    con.close()


def save_attempt(user_id, raw, normalized, recognized, spell, score):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("INSERT INTO attempts (user_id, ts, raw, normalized, recognized, spell, score) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, datetime.utcnow().isoformat(), raw, normalized, int(recognized), spell, score))
    con.commit()
    con.close()
