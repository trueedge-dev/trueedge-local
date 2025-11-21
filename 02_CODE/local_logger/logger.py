import json
from pathlib import Path
from datetime import datetime, timezone

# Path to the "data" folder inside this local_logger directory
DATA_DIR = Path(__file__).resolve().parent / "data"

# Log file where new TRADE_EVENTs will be appended
LOG_FILE = DATA_DIR / "trades_log.jsonl"


def append_trade_event(event: dict) -> None:
    """
    Append a single TRADE_EVENT object to the log file as one JSON line.

    This function assumes the event follows the TRADE_EVENT_SPEC core fields.
    It does a simple required-field check and then appends the event to LOG_FILE.
    """
    required_fields = [
        "event_id",
        "account_id",
        "strategy_id",
        "environment",
        "venue",
        "timestamp",
        "symbol",
        "side",
        "order_type",
        "quantity",
        "quantity_type",
        "price_open",
        "price_close",
        "fees",
        "pnl",
        "state",
    ]

    missing = [field for field in required_fields if field not in event]
    if missing:
        raise ValueError(f"Missing required fields in TRADE_EVENT: {missing}")

    # Make sure the data directory exists
    DATA_DIR.mkdir(exist_ok=True)

    # Open the log file in append mode and write one JSON object per line
    with LOG_FILE.open("a", encoding="utf-8") as f:
        json.dump(event, f, ensure_ascii=False)
        f.write("\n")


def build_demo_event() -> dict:
    """
    Build a single demo TRADE_EVENT object that follows our specification.

    This is just for testing the logger and will be refined or replaced later.
    """
    now = datetime.now(timezone.utc)
    ts = now.isoformat().replace("+00:00", "Z")

    return {
        "event_id": f"evt_{ts}",
        "account_id": "acc_demo_001",
        "strategy_id": "strat_demo_v1",
        "environment": "demo",
        "venue": "DEMO-PLATFORM",
        "timestamp": ts,
        "symbol": "XAUUSD",
        "side": "buy",
        "order_type": "market",
        "quantity": 0.10,
        "quantity_type": "lots",
        "price_open": 2380.00,
        "price_close": 2381.50,
        "fees": -1.00,
        "pnl": 14.00,
        "state": "closed",
        "linked_position_id": "pos_demo_001",
        "tags": ["demo", "xau"],
        "metadata": {
            "notes": "Demo trade event from logger.py"
        },
    }


def main() -> None:
    """
    Entry point for manual testing.

    - Creates the data directory if needed.
    - Builds one demo TRADE_EVENT.
    - Appends it to trades_log.jsonl.
    - Prints basic info to the console.
    """
    event = build_demo_event()
    append_trade_event(event)
    print(f"Appended trade event: {event['event_id']}")
    print(f"Log file location: {LOG_FILE}")


if __name__ == "__main__":
    main()
