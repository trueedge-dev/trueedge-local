import json
from urllib import request


def build_demo_event() -> dict:
    """
    Build a demo TRADE_EVENT suitable for sending to the backend.
    """
    return {
        "event_id": "backend_demo_001",
        "account_id": "acc_backend_001",
        "strategy_id": "strat_backend_demo_v1",
        "environment": "demo",
        "venue": "XAUUSD",
        "timestamp": "2025-01-01T12:00:00+00:00",
        "symbol": "XAUUSD",
        "side": "buy",
        "order_type": "market",
        "quantity": 0.1,
        "quantity_type": "lots",
        "price_open": 2000.0,
        "price_close": 2005.0,
        "fees": 0.5,
        "pnl": 4.5,
        "state": "closed",
    }


def main() -> None:
    url = "http://127.0.0.1:9000/trade_event"
    event = build_demo_event()
    data = json.dumps(event).encode("utf-8")

    req = request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    print(f"Sending demo TRADE_EVENT to {url} ...")
    try:
        with request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            print("Response status:", resp.status)
            print("Response body:", body)
    except Exception as e:
        print("Request failed:", e)


if __name__ == "__main__":
    main()
