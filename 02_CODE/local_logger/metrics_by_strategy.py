from pathlib import Path

from metrics_core import load_events, compute_metrics, group_by_key


DATA_DIR = Path(__file__).resolve().parent / "data"
LOG_FILE = DATA_DIR / "trades_log.jsonl"


def print_metrics_block(title: str, metrics: dict):
    """
    Pretty-print metrics with a title.
    """
    print(title)
    print("-" * len(title))
    for key, value in metrics.items():
        print(f"{key}: {value}")
    print()


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
