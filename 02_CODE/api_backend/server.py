import json
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path

import db


# Make sure we can import shared modules from local_logger
ROOT_DIR = Path(__file__).resolve().parents[1]  # .../02_CODE
LOCAL_LOGGER_DIR = ROOT_DIR / "local_logger"
if str(LOCAL_LOGGER_DIR) not in sys.path:
    sys.path.insert(0, str(LOCAL_LOGGER_DIR))

from trade_event_validator import validate_trade_event, TradeEventValidationError
from metrics_core import compute_metrics, group_by_key


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


class TrueedgeBackendHandler(BaseHTTPRequestHandler):
    def _send_json(self, status_code: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, status_code: int, html: str) -> None:
        body = html.encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/health":
            self._send_json(200, {"status": "ok", "service": "trueedge_backend"})
            return

        if path == "/metrics/overall":
            query = parse_qs(parsed.query)
            account_id = query.get("account_id", [None])[0]
            strategy_id = query.get("strategy_id", [None])[0]

            events = db.fetch_events(account_id=account_id, strategy_id=strategy_id)
            metrics = compute_metrics(events, starting_balance=0.0)
            response = {
                "status": "ok",
                "filters": {
                    "account_id": account_id,
                    "strategy_id": strategy_id,
                },
                "count": len(events),
                "metrics": metrics,
            }
            self._send_json(200, response)
            return

        if path == "/metrics/by_strategy":
            query = parse_qs(parsed.query)
            account_id = query.get("account_id", [None])[0]

            events = db.fetch_events(account_id=account_id, strategy_id=None)
            groups = group_by_key(events, "strategy_id")

            strategies = []
            for strat_id, strat_events in groups.items():
                m = compute_metrics(strat_events, starting_balance=0.0)
                strategies.append(
                    {
                        "strategy_id": strat_id,
                        "count": len(strat_events),
                        "metrics": m,
                    }
                )

            response = {
                "status": "ok",
                "filters": {"account_id": account_id},
                "strategies": strategies,
            }
            self._send_json(200, response)
            return

        if path == "/metrics/by_account":
            query = parse_qs(parsed.query)
            strategy_id = query.get("strategy_id", [None])[0]

            events = db.fetch_events(account_id=None, strategy_id=strategy_id)
            groups = group_by_key(events, "account_id")

            accounts = []
            for acc_id, acc_events in groups.items():
                m = compute_metrics(acc_events, starting_balance=0.0)
                accounts.append(
                    {
                        "account_id": acc_id,
                        "count": len(acc_events),
                        "metrics": m,
                    }
                )

            response = {
                "status": "ok",
                "filters": {"strategy_id": strategy_id},
                "accounts": accounts,
            }
            self._send_json(200, response)
            return

        if path == "/report":
            query = parse_qs(parsed.query)
            account_id = query.get("account_id", [None])[0]
            strategy_id = query.get("strategy_id", [None])[0]

            events = db.fetch_events(account_id=account_id, strategy_id=strategy_id)
            overall_metrics = compute_metrics(events, starting_balance=0.0)

            by_strategy = group_by_key(events, "strategy_id")
            strat_blocks = []
            for strat_id, strat_events in by_strategy.items():
                m = compute_metrics(strat_events, starting_balance=0.0)
                strat_blocks.append(metrics_table_html(f"strategy_id = {strat_id}", m))

            by_account = group_by_key(events, "account_id")
            acc_blocks = []
            for acc_id, acc_events in by_account.items():
                m = compute_metrics(acc_events, starting_balance=0.0)
                acc_blocks.append(metrics_table_html(f"account_id = {acc_id}", m))

            filters_desc = []
            if account_id:
                filters_desc.append(f"account_id = {account_id}")
            if strategy_id:
                filters_desc.append(f"strategy_id = {strategy_id}")
            filters_text = ", ".join(filters_desc) if filters_desc else "none"

            html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <title>TRUEEDGE Backend Report</title>
</head>
<body>
  <h1>TRUEEDGE Backend Report</h1>
  <p>This report is generated from the SQLite database (trueedge_backend.db).</p>
  <p><strong>Filters:</strong> {filters_text}</p>

  {metrics_table_html("OVERALL metrics (from backend DB)", overall_metrics)}

  <h2>Metrics by strategy_id</h2>
  {''.join(strat_blocks) if strat_blocks else "<p>No strategy data.</p>"}

  <h2>Metrics by account_id</h2>
  {''.join(acc_blocks) if acc_blocks else "<p>No account data.</p>"}

  <p style="margin-top: 20px; font-size: 12px; color: #555;">
    Served by TRUEEDGE backend API at /report.
  </p>
</body>
</html>
"""
            self._send_html(200, html_content)
            return

        # If we reach here, endpoint is not found
        self._send_json(404, {"status": "error", "message": "Not found"})

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        if path != "/trade_event":
            self._send_json(404, {"status": "error", "message": "Not found"})
            return

        content_length = self.headers.get("Content-Length")
        try:
            length = int(content_length) if content_length is not None else 0
        except ValueError:
            self._send_json(400, {"status": "error", "message": "Invalid Content-Length"})
            return

        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode("utf-8"))
        except json.JSONDecodeError as e:
            self._send_json(400, {"status": "error", "message": f"Invalid JSON: {e}"})
            return

        # Validate TRADE_EVENT
        try:
            validate_trade_event(payload)
        except TradeEventValidationError as e:
            self._send_json(400, {"status": "error", "message": f"Invalid TRADE_EVENT: {e}"})
            return

        # Insert into DB
        try:
            db.insert_trade_event(payload)
        except ValueError as e:
            self._send_json(400, {"status": "error", "message": str(e)})
            return
        except Exception as e:
            self._send_json(500, {"status": "error", "message": f"Internal error: {e}"})
            return

        self._send_json(200, {"status": "ok"})

    # Reduce default noisy logging
    def log_message(self, format: str, *args) -> None:
        sys.stdout.write(
            "%s - - [%s] %s\n"
            % (self.client_address[0], self.log_date_time_string(), format % args)
        )


def main() -> None:
    db.init_db()
    server_address = ("127.0.0.1", 9000)
    httpd = HTTPServer(server_address, TrueedgeBackendHandler)
    print("TRUEEDGE backend API running on http://127.0.0.1:9000")
    print("Endpoints:")
    print("  GET  /health")
    print("  POST /trade_event")
    print("  GET  /metrics/overall?account_id=...&strategy_id=...")
    print("  GET  /metrics/by_strategy?account_id=...")
    print("  GET  /metrics/by_account?strategy_id=...")
    print("  GET  /report?account_id=...&strategy_id=...")
    print("Press Ctrl+C to stop.")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping TRUEEDGE backend API...")
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
