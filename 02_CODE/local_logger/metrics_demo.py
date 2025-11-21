import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).resolve().parent / "data"
LOG_FILE = DATA_DIR / "trades_log.jsonl"
EXAMPLE_FILE = DATA_DIR / "example_trades.jsonl"


def load_events(path: Path):
    """
    Load TRADE_EVENT objects from a .jsonl file.
    Returns a list of dicts. If file does not exist, returns an empty list.
    """
    events = []
    if not path.exists():
        print(f"[INFO] No file found at {path}")
        return events

    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as e:
                print(f"[WARN] Skipping invalid line in {path.name}: {e}")
    return events


def sort_events(events):
    """
    Sort events by their timestamp field (ISO 8601 expected).
    If parsing fails, those events fall back to minimal datetime.
    """
    def parse_ts(ev):
        ts = ev.get("timestamp")
        if not ts:
            return datetime.min
        try:
            # Handle timestamps ending with 'Z' (UTC)
            if ts.endswith("Z"):
                ts = ts.replace("Z", "+00:00")
            return datetime.fromisoformat(ts)
        except Exception:
            return datetime.min

    return sorted(events, key=parse_ts)


def compute_metrics(events, starting_balance=0.0):
    """
    Compute simple metrics from a list of TRADE_EVENT dicts:
    - total_trades
    - total_pnl
    - ending_equity
    - max_drawdown (simple peak-to-trough)
    - wins, losses, win_rate
    """
    total_trades = len(events)
    total_pnl = 0.0
    equity = starting_balance
    equity_points = []

    for ev in sort_events(events):
        pnl = float(ev.get("pnl", 0.0))
        total_pnl += pnl
        equity += pnl
        equity_points.append(equity)

    max_drawdown = 0.0
    if equity_points:
        peak = equity_points[0]
        for eq in equity_points:
            if eq > peak:
                peak = eq
            drawdown = peak - eq
            if drawdown > max_drawdown:
                max_drawdown = drawdown

    wins = sum(1 for ev in events if float(ev.get("pnl", 0.0)) > 0)
    losses = sum(1 for ev in events if float(ev.get("pnl", 0.0)) < 0)
    win_rate = (wins / total_trades * 100.0) if total_trades > 0 else 0.0

    return {
        "total_trades": total_trades,
        "total_pnl": round(total_pnl, 2),
        "ending_equity": round(starting_balance + total_pnl, 2),
        "max_drawdown": round(max_drawdown, 2),
        "wins": wins,
        "losses": losses,
        "win_rate": round(win_rate, 2),
    }


def print_metrics(title: str, metrics: dict):
    """
    Pretty-print metrics with a title.
    """
    print(title)
    print("-" * len(title))
    for key, value in metrics.items():
        print(f"{key}: {value}")
    print()


def main():
    print("TRUEEDGE metrics demo")
    print("=" * 30)

    example_events = load_events(EXAMPLE_FILE)
    log_events = load_events(LOG_FILE)

    if example_events:
        metrics_example = compute_metrics(example_events, starting_balance=0.0)
        print_metrics(f"Metrics for {EXAMPLE_FILE.name}", metrics_example)
    else:
        print(f"[INFO] No events found in {EXAMPLE_FILE}")

    if log_events:
        metrics_log = compute_metrics(log_events, starting_balance=0.0)
        print_metrics(f"Metrics for {LOG_FILE.name}", metrics_log)
    else:
        print(f"[INFO] No events found in {LOG_FILE}")
        print("[HINT] Run logger.py at least once to generate a demo event.")


if __name__ == "__main__":
    main()
