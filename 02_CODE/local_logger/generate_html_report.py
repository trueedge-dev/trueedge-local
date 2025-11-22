from pathlib import Path
from collections import defaultdict

from metrics_core import load_events, compute_metrics, group_by_key


DATA_DIR = Path(__file__).resolve().parent / "data"
LOG_FILE = DATA_DIR / "trades_log.jsonl"
REPORTS_DIR = Path(__file__).resolve().parent / "reports"


def metrics_table_html(title: str, metrics: dict) -> str:
    """
    Create a simple HTML table from a metrics dict.
    """
    rows = "\n".join(
        f"<tr><td>{key}</td><td>{value}</td></tr>"
        for key, value in metrics.items()
    )
    return f"""
    <h3>{title}</h3>
    <table border="1" cellspacing="0" cellpadding="4">
      <tbody>
        {rows}
      </tbody>
    </table>
    """


def main():
    print("Generating TRUEEDGE HTML report...")

    events = load_events(LOG_FILE)
    if not events:
        print(f"[INFO] No events found in {LOG_FILE}")
        print("[HINT] Run logger.py, simulate_trades.py, or send_test_trade.py first.")
        return

    # Ensure reports directory exists
    REPORTS_DIR.mkdir(exist_ok=True)

    # Overall metrics
    overall_metrics = compute_metrics(events, starting_balance=0.0)

    # By strategy_id
    by_strategy = group_by_key(events, "strategy_id")
    strategy_blocks = []
    for strat_id, strat_events in by_strategy.items():
        m = compute_metrics(strat_events, starting_balance=0.0)
        strategy_blocks.append(metrics_table_html(f"strategy_id = {strat_id}", m))

    # By account_id
    by_account = group_by_key(events, "account_id")
    account_blocks = []
    for acc_id, acc_events in by_account.items():
        m = compute_metrics(acc_events, starting_balance=0.0)
        account_blocks.append(metrics_table_html(f"account_id = {acc_id}", m))

    # Build full HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>TRUEEDGE Local Report</title>
</head>
<body>
  <h1>TRUEEDGE Local Report</h1>
  <p>This report is generated from trades_log.jsonl in the local_logger/data folder.</p>

  {metrics_table_html("OVERALL metrics for trades_log.jsonl", overall_metrics)}

  <h2>Metrics by strategy_id</h2>
  {''.join(strategy_blocks)}

  <h2>Metrics by account_id</h2>
  {''.join(account_blocks)}

  <p style="margin-top: 20px; font-size: 12px; color: #555;">
    Generated locally by generate_html_report.py.
  </p>
</body>
</html>
"""

    report_path = REPORTS_DIR / "index.html"
    report_path.write_text(html_content, encoding="utf-8")

    print(f"Report generated at: {report_path}")
    print("You can open this file in your browser (double-click in Explorer).")


if __name__ == "__main__":
    main()
