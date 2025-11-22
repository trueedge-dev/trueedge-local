TRUEEDGE – API BACKEND PROTOTYPE

PURPOSE:
This folder will contain the first backend prototype for TRUEEDGE.

It will evolve from the local logger into a service that can:

- receive TRADE_EVENT objects over HTTP,
- validate and store them in a SQLite database,
- compute and serve metrics via JSON endpoints,
- serve simple HTML reports.

Current status:
- Planning phase only (see 01_DOCS/BACKEND_PROTO_PLAN.txt).
- No backend server implementation yet.

Planned components (draft):
- app.py or server.py
    - starts HTTP server on localhost (e.g. port 9000)
    - defines endpoints:
        - POST /trade_event
        - GET /metrics/overall
        - GET /metrics/by_strategy
        - GET /metrics/by_account
        - GET /report
- db.py
    - handles SQLite connection and schema (trades table)
- reuse of:
    - trade_event_validator (from shared core)
    - metrics_core (for metrics computation over DB data)

This backend will first run locally on the same machine, then later move toward
a simple cloud deployment as TRUEEDGE Cloud prototype.
