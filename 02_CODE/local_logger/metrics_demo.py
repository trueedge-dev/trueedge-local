from pathlib import Path

from metrics_core import load_events, compute_metrics


DATA_DIR = Path(__file__).resolve().parent / "data"
LOG_FILE = DATA_DIR / "trades_log.jsonl"
EXAMPLE_FILE = DATA_DIR / "example_trades.jsonl"


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
        print("[HINT] Run logger.py, simulate_trades.py, or send_test_trade.py first.")


if __name__ == "__main__":
    main()
