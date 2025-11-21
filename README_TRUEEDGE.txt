TRUEEDGE – Verifiable Strategy Exchange (Local Prototype)

WHAT THIS PROJECT IS:
TRUEEDGE is an infrastructure and marketplace concept for trading strategies where every performance number is tied to real, verifiable trade logs.

This folder currently contains a very early local prototype:
- 01_DOCS:
    - TRUEEDGE_VISION.txt – high-level description of the project.
    - TRADE_EVENT_SPEC.txt – draft specification of the TRADE_EVENT data model.
- 02_CODE:
    - local_logger/
        - README_LOCAL_LOGGER.txt – overview of the local logging component.
        - data/
            - example_trades.jsonl – sample TRADE_EVENT objects.
            - trades_log.jsonl – log file created by logger.py (demo trades).
        - logger.py – script for appending TRADE_EVENT objects to trades_log.jsonl.
        - metrics_demo.py – script for computing simple metrics from trade logs.
- Other folders (03_MARKET, 04_INFRA, 05_LOGS) are reserved for future work.

CURRENT STATUS (LOCAL PROTOTYPE):
- We can define TRADE_EVENT objects in a JSON-lines format (.jsonl).
- We can append demo events to a log file using logger.py.
- We can compute simple metrics (total trades, total PnL, equity, max drawdown, win rate) using metrics_demo.py.

NEXT STEPS (HIGH LEVEL):
- Refine the TRADE_EVENT schema.
- Extend the local logger into a more general logging service.
- Begin designing a cloud backend and API for receiving and serving verified trade logs.
