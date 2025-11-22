import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional


DB_PATH = Path(__file__).resolve().parent / "trueedge_backend.db"


def get_connection() -> sqlite3.Connection:
    """
    Open a connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)


def init_db() -> None:
    """
    Create the trades table if it does not exist.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                event_id TEXT UNIQUE,
                account_id TEXT,
                strategy_id TEXT,
                environment TEXT,
                venue TEXT,
                timestamp TEXT,
                symbol TEXT,
                side TEXT,
                order_type TEXT,
                quantity REAL,
                quantity_type TEXT,
                price_open REAL,
                price_close REAL,
                fees REAL,
                pnl REAL,
                state TEXT,
                raw_json TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def insert_trade_event(event: Dict[str, Any]) -> None:
    """
    Insert a validated TRADE_EVENT into the trades table.

    Raises ValueError if the event_id already exists.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO trades (
                event_id,
                account_id,
                strategy_id,
                environment,
                venue,
                timestamp,
                symbol,
                side,
                order_type,
                quantity,
                quantity_type,
                price_open,
                price_close,
                fees,
                pnl,
                state,
                raw_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(event.get("event_id")),
                str(event.get("account_id")),
                str(event.get("strategy_id")),
                str(event.get("environment")),
                str(event.get("venue")),
                str(event.get("timestamp")),
                str(event.get("symbol")),
                str(event.get("side")),
                str(event.get("order_type")),
                float(event.get("quantity", 0.0)),
                str(event.get("quantity_type")),
                float(event.get("price_open", 0.0)),
                float(event.get("price_close", 0.0)),
                float(event.get("fees", 0.0)),
                float(event.get("pnl", 0.0)),
                str(event.get("state")),
                json.dumps(event),
            ),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Event with this event_id already exists in database")
    finally:
        conn.close()


def fetch_events(
    account_id: Optional[str] = None,
    strategy_id: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Fetch events from the trades table, optionally filtered by account_id/strategy_id.
    Returns a list of TRADE_EVENT dicts reconstructed from raw_json.
    """
    conn = get_connection()
    try:
        cur = conn.cursor()
        query = "SELECT raw_json FROM trades"
        conditions = []
        params: List[Any] = []

        if account_id:
            conditions.append("account_id = ?")
            params.append(account_id)
        if strategy_id:
            conditions.append("strategy_id = ?")
            params.append(strategy_id)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        cur.execute(query, params)
        rows = cur.fetchall()

        events: List[Dict[str, Any]] = []
        for (raw_json,) in rows:
            try:
                events.append(json.loads(raw_json))
            except json.JSONDecodeError:
                # Skip rows with invalid JSON (should not happen, but be safe)
                continue

        return events
    finally:
        conn.close()
