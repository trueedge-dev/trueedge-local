LOCAL LOGGER – OVERVIEW (TRUEEDGE)

WHAT THIS FOLDER IS FOR:
This "local_logger" component is the first prototype of TRUEEDGE.
Its job is simple:

- take TRADE_EVENT objects (following TRADE_EVENT_SPEC),
- write them to local files on disk in .jsonl format,
- read them back and compute simple performance metrics.

We start with a very basic local file-based logger before moving to any cloud or database.
This keeps everything simple and under full control.

FOLDER STRUCTURE (current):

- local_logger/
    - README_LOCAL_LOGGER.txt   <-- this file
    - data/
        - example_trades.jsonl  <-- sample file with example TRADE_EVENT objects
        - trades_log.jsonl      <-- log file created by logger.py and simulate_trades.py
    - logger.py                 <-- appends single TRADE_EVENT objects to trades_log.jsonl
    - metrics_demo.py           <-- reads .jsonl files and prints simple metrics
    - simulate_trades.py        <-- generates multiple demo TRADE_EVENTs and logs them

FILE ROLES (DETAIL):

1) data/example_trades.jsonl
   - Contains a few hand-crafted TRADE_EVENT objects.
   - Used as a static example for metrics_demo.py.

2) data/trades_log.jsonl
   - Main log file for demo runs.
   - logger.py appends one demo TRADE_EVENT when run.
   - simulate_trades.py appends many simulated trades for testing.

3) logger.py
   - Provides append_trade_event(event: dict) which:
       - checks required fields,
       - appends the event as one JSON line to trades_log.jsonl.
   - When run directly (python logger.py), it:
       - builds a single demo TRADE_EVENT,
       - appends it to trades_log.jsonl,
       - prints basic info.

4) simulate_trades.py
   - Uses append_trade_event from logger.py.
   - Builds many simulated TRADE_EVENT objects (currently 20 by default) with:
       - slightly randomized prices,
       - simple PnL calculation,
       - demo timestamps.
   - When run directly (python simulate_trades.py), it:
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

NEXT STEPS (LOCAL LOGGER ROADMAP – HIGH LEVEL):
- Refine the TRADE_EVENT schema and validation.
- Add simple configuration (e.g., choose output file names, accounts, strategies).
- Evolve this local logger into:
    - a small HTTP service that accepts TRADE_EVENTs via API,
    - a component that can be called from real trading connectors (MT5, exchanges, etc.).

