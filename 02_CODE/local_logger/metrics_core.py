import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any


def load_events(path: Path) -> List[Dict[str, Any]]:
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


def sort_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sort events by their timestamp field (ISO 8601 expected).
    If parsing fails, those events fall back to minimal datetime.
    """

    def parse_ts(ev: Dict[str, Any]) -> datetime:
        ts = ev.get("timestamp")
        if not ts:
            return datetime.min
        try:
            if isinstance(ts, str) and ts.endswith("Z"):
                ts = ts.replace("Z", "+00:00")
            return datetime.fromisoformat(ts)
        except Exception:
            return datetime.min

    return sorted(events, key=parse_ts)


def compute_metrics(
    events: List[Dict[str, Any]], starting_balance: float = 0.0
) -> Dict[str, Any]:
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
    equity_points: List[float] = []

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


def group_by_key(events: List[Dict[str, Any]], key_name: str) -> Dict[str, List[Dict[str, Any]]]:
    """
    Group events by a specific key in the event dict.
    Returns a dict: key_value -> list of events.
    """
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for ev in events:
        key_value = ev.get(key_name, "<UNKNOWN>")
        groups.setdefault(str(key_value), []).append(ev)
    return groups
