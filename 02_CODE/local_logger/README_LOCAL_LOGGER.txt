LOCAL LOGGER – OVERVIEW (TRUEEDGE)

WHAT THIS FOLDER IS FOR:
This "local_logger" component is the first prototype of TRUEEDGE.
Its job is to:

- accept TRADE_EVENT objects (following TRADE_EVENT_SPEC),
- write them to local files on disk in .jsonl format,
- read them back and compute simple performance metrics.

We start with a very basic local file-based logger and then evolve it towards
a local HTTP service and, later, a cloud backend.

FOLDER STRUCTURE (current):

- local_logger/
    - README_LOCAL_LOGGER.txt     <-- this file
    - data/
        - example_trades.jsonl    <-- sample file with example TRADE_EVENT objects
        - trades_log.jsonl        <-- main log file created by logger/sim/service
    - logger.py                   <-- core append_trade_event() + single demo write
    - simulate_trades.py          <-- generates multiple demo TRADE_EVENTs and logs them
    - metrics_demo.py             <-- reads .jsonl files and prints simple metrics
    - logger_service.py           <-- local HTTP service (POST /trade_event)
    - send_test_trade.py          <-- client script that sends one TRADE_EVENT via HTTP

FILE ROLES (DETAIL):

1) data/example_trades.jsonl
   - Contains a few hand-crafted TRADE_EVENT objects.
   - Used as a static example for metrics_demo.py.

2) data/trades_log.jsonl
   - Main log file for demo runs.
   - logger.py appends one demo TRADE_EVENT when run directly.
   - simulate_trades.py appends many simulated trades for testing.
   - logger_service.py appends events received via HTTP.
   - send_test_trade.py proves the HTTP path by sending a demo event.

3) logger.py
   - Provides:
       - append_trade_event(event: dict):
           - checks required fields,
           - appends the event as one JSON line to trades_log.jsonl.
   - When run directly:
       - builds a single demo TRADE_EVENT,
       - appends it to trades_log.jsonl,
       - prints basic info (event_id, log file location).

4) simulate_trades.py
   - Uses append_trade_event from logger.py.
   - Builds many simulated TRADE_EVENT objects (default: 20) with:
       - slightly randomized prices,
       - simple PnL calculation,
       - demo timestamps.
   - When run directly:
       - appends num_trades events to trades_log.jsonl,
       - prints how many trades were logged.

5) metrics_demo.py
   - Loads TRADE_EVENT objects from:
       - example_trades.jsonl
       - trades_log.jsonl
   - Sorts events by timestamp.
   - Computes:
       - total_trades,
       - total_pnl,
       - ending_equity,
       - max_drawdown (simple peak-to-trough),
       - wins, losses, win_rate.
   - Prints metrics for each file.

6) logger_service.py
   - Implements a simple local HTTP service using Python's standard library.
   - Starts an HTTP server on http://127.0.0.1:8080
   - Exposes:
       - POST /trade_event
           - expects JSON body representing a TRADE_EVENT,
           - validates required fields via append_trade_event,
           - appends to trades_log.jsonl,
           - returns JSON like: {"status": "ok"} or an error.

7) send_test_trade.py
   - Builds a demo TRADE_EVENT in Python.
   - Sends it as JSON via HTTP POST to:
       - http://127.0.0.1:8080/trade_event
   - Prints response status and body.
   - Used to test the local logger_service HTTP endpoint.

HOW TO USE (SUMMARY):

1) Log a single demo event directly with logger.py:
   - cd to local_logger
   - run: python logger.py

2) Log multiple simulated trades:
   - cd to local_logger
   - run: python simulate_trades.py

3) Start the local HTTP logger service:
   - cd to local_logger
   - run: python logger_service.py
   - keep this window open (service running)

4) In another terminal, send a demo TRADE_EVENT over HTTP:
   - cd to local_logger
   - run: python send_test_trade.py
   - check that it prints {"status": "ok"}

5) View metrics:
   - cd to local_logger
   - run: python metrics_demo.py
   - see total_trades, total_pnl, max_drawdown, etc.

NEXT STEPS (LOCAL LOGGER ROADMAP – HIGH LEVEL):
- Refine the TRADE_EVENT schema and validation (stricter checks, types).
- Add simple configuration (choose accounts, strategies, log files).
- Turn the local HTTP service into a more general logging service (possibly
  with multiple endpoints and basic authentication).
- Use this HTTP interface as the target for future trading platform connectors
  (MT5, exchanges, etc.), and later move the same API shape into a cloud backend.
