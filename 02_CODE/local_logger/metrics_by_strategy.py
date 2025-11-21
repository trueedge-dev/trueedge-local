import json
from pathlib import Path
from datetime import datetime
from collections import defaultdict


DATA_DIR = Path(__file__).resolve().parent / "data"
LOG_FILE = DATA_DIR / "trades_log.jsonl"


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


def print_metrics_block(title: str, metrics: dict):
    """
    Pretty-print metrics with a title.
    """
    print(title)
    print("-" * len(title))
    for key, value in metrics.items():
        print(f"{key}: {value}")
    print()


def group_by_key(events, key_name: str):
    """
    Group events by a specific key in the event dict.
    Returns a dict: key_value -> list of events.
    """
    groups = defaultdict(list)
    for ev in events:
        key_value = ev.get(key_name, "<UNKNOWN>")
        groups[key_value].append(ev)
    return groups


def main():
    print("TRUEEDGE metrics by strategy/account")
    print("=" * 40)

    events = load_events(LOG_FILE)
    if not events:
        print(f"[INFO] No events found in {LOG_FILE}")
        print("[HINT] Run logger.py, simulate_trades.py, or send_test_trade.py first.")
        return

    # Overall metrics
    overall_metrics = compute_metrics(events, starting_balance=0.0)
    print_metrics_block(f"OVERALL metrics for {LOG_FILE.name}", overall_metrics)

    # Metrics by strategy_id
    print("Metrics by strategy_id")
    print("----------------------")
    by_strategy = group_by_key(events, "strategy_id")
    for strat_id, strat_events in by_strategy.items():
        m = compute_metrics(strat_events, starting_balance=0.0)
        print_metrics_block(f"strategy_id = {strat_id}", m)

    # Metrics by account_id
    print("Metrics by account_id")
    print("---------------------")
    by_account = group_by_key(events, "account_id")
    for acc_id, acc_events in by_account.items():
        m = compute_metrics(acc_events, starting_balance=0.0)
        print_metrics_block(f"account_id = {acc_id}", m)


if __name__ == "__main__":
    main()
