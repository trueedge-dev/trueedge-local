import json
from datetime import datetime, timezone
from urllib import request, error


def build_demo_event() -> dict:
    """
    Build a demo TRADE_EVENT object to send to the logger service.
    """
    ts = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    return {
        "event_id": f"evt_http_demo_{ts}",
        "account_id": "acc_demo_http_001",
        "strategy_id": "strat_http_demo_v1",
        "environment": "demo",
        "venue": "HTTP-DEMO",
        "timestamp": ts,
        "symbol": "XAUUSD",
        "side": "buy",
        "order_type": "market",
        "quantity": 0.10,
        "quantity_type": "lots",
        "price_open": 2380.00,
        "price_close": 2382.50,
        "fees": -1.00,
        "pnl": 24.00,
        "state": "closed",
        "linked_position_id": "pos_http_demo_0001",
        "tags": ["http_demo", "xau"],
        "metadata": {
            "notes": "Demo trade sent via send_test_trade.py"
        },
    }


def send_trade_event(event: dict, url: str = "http://127.0.0.1:8080/trade_event") -> None:
    """
    Send a TRADE_EVENT as JSON via HTTP POST to the logger service.
    """
    data = json.dumps(event).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            print(f"Response status: {resp.status}")
            print(f"Response body: {body}")
    except error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}")
        try:
            err_body = e.read().decode("utf-8")
            print(f"Error body: {err_body}")
        except Exception:
            pass
    except error.URLError as e:
        print(f"Connection error: {e.reason}")


def main() -> None:
    event = build_demo_event()
    print("Sending demo TRADE_EVENT to logger service...")
    send_trade_event(event)


if __name__ == "__main__":
    main()
