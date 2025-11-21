import random
from datetime import datetime, timedelta, timezone
from pathlib import Path

from logger import append_trade_event

DATA_DIR = Path(__file__).resolve().parent / "data"


def build_simulated_event(index: int, base_time: datetime) -> dict:
    """
    Build a simulated TRADE_EVENT.

    We keep it simple:
    - instrument: XAUUSD
    - environment: demo
    - venue: DEMO-SIM
    - strategy: strat_sim_v1
    - each trade is spaced a few minutes apart in time
    """
    # Time: base_time + index * 5 minutes
    ts_dt = base_time + timedelta(minutes=5 * index)
    ts = ts_dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")

    side = random.choice(["buy", "sell"])
    quantity = 0.10
    quantity_type = "lots"

    # Simple price simulation around a center price
    center_price = 2380.0
    price_open = center_price + random.uniform(-10, 10)
    # Move a bit in either direction
    price_move = random.uniform(-5, 5)
    price_close = price_open + price_move

    # Rough PnL approximation: assume 1 lot ≈ $1 per $1 move for simplicity,
    # so 0.10 lots ≈ $0.10 per $1 move. This is NOT realistic, but good enough
    # for a demo. We also subtract a fixed fee.
    fee = -1.00
    gross_pnl = (price_close - price_open) * (0.10) * 100  # magnify a bit
    pnl = gross_pnl + fee

    event_id = f"evt_sim_{ts}_{index:04d}"

    return {
        "event_id": event_id,
        "account_id": "acc_demo_sim_001",
        "strategy_id": "strat_sim_v1",
        "environment": "demo",
        "venue": "DEMO-SIM",
        "timestamp": ts,
        "symbol": "XAUUSD",
        "side": side,
        "order_type": "market",
        "quantity": quantity,
        "quantity_type": quantity_type,
        "price_open": round(price_open, 2),
        "price_close": round(price_close, 2),
        "fees": round(fee, 2),
        "pnl": round(pnl, 2),
        "state": "closed",
        "linked_position_id": f"pos_sim_{index:04d}",
        "tags": ["demo_sim", "xau"],
        "metadata": {
            "notes": "Simulated trade from simulate_trades.py"
        },
    }


def simulate_trades(num_trades: int = 20) -> None:
    """
    Generate num_trades simulated TRADE_EVENTs and append them to trades_log.jsonl
    using append_trade_event from logger.py.
    """
    base_time = datetime.now(timezone.utc) - timedelta(minutes=5 * num_trades)

    for i in range(num_trades):
        event = build_simulated_event(i, base_time)
        append_trade_event(event)
    print(f"Simulated and logged {num_trades} trades.")


def main() -> None:
    """
    Entry point:
    - Simulate 20 trades by default.
    """
    simulate_trades(num_trades=20)


if __name__ == "__main__":
    main()
