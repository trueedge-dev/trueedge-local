LOCAL LOGGER – OVERVIEW (TRUEEDGE)

WHAT THIS FOLDER IS FOR:
This "local_logger" component is the first prototype of TRUEEDGE.
Its job is simple:

- take TRADE_EVENT objects (following TRADE_EVENT_SPEC),
- write them to a local file on disk,
- later allow us to read them back and compute metrics (equity curve, PnL, etc.).

We start with a very basic local file-based logger before moving to any cloud or database.
This keeps everything simple and under full control.

FOLDER STRUCTURE (planned):

- local_logger/
    - README_LOCAL_LOGGER.txt   <-- this file
    - data/
        - example_trades.jsonl  <-- sample file with example TRADE_EVENT objects
    - (later) logger.py         <-- Python script for writing TRADE_EVENTs
    - (later) metrics_demo.py   <-- Python script for computing simple metrics

NOTES:
- "jsonl" means JSON Lines: one JSON object per line in the file.
- Each line will represent one TRADE_EVENT.
- This format is easy to append to and easy to process later.

NEXT STEPS (FUTURE CHUNKS):
- Fill data/example_trades.jsonl with a small set of example trades.
- Write logger.py that can append TRADE_EVENT objects to a jsonl file.
- Write metrics_demo.py that reads TRADE_EVENT objects and calculates:
  - cumulative PnL,
  - equity over time,
  - max drawdown (simple version).

