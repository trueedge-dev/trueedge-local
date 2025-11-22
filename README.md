\# TRUEEDGE – Verifiable Strategy Exchange (Local Prototype)



TRUEEDGE is an infrastructure and marketplace concept for trading strategies where every

performance number is tied to \*\*real, verifiable trade logs\*\*.



This repository currently contains a \*\*local prototype\*\* that runs on one machine and proves

the core ideas:



\- a structured `TRADE\_EVENT` data model,

\- an append-only logger (file-based),

\- basic metrics and reports,

\- a local HTTP logging service.



---



\## Project Layout



At the root:



\- `README.md` – this file (GitHub-friendly overview)

\- `README\_TRUEEDGE.txt` – additional overview text

\- `.gitignore` – Git ignore rules

\- `01\_DOCS/` – documents, specs, and plans

\- `02\_CODE/` – all code (for now)

\- `03\_MARKET/` – reserved for future marketplace logic

\- `04\_INFRA/` – reserved for deployment/infra scripts

\- `05\_LOGS/` – reserved for system logs later



\### 01\_DOCS/



Key documents:



\- `TRUEEDGE\_VISION.txt` – high-level narrative of what TRUEEDGE is

\- `TRADE\_EVENT\_SPEC.txt` – TRADE\_EVENT data model specification

\- `LOGGER\_SERVICE\_PLAN.txt` – evolution plan: local logger → local HTTP service → cloud backend

\- `TRUEEDGE\_MONEY\_PLAN.txt` – monetization paths and realistic phases

\- `CODE\_STRUCTURE\_PLAN.txt` – how the codebase is organized and will evolve

\- `LOCAL\_QUICKSTART.txt` – concrete steps to run the local prototype



\### 02\_CODE/local\_logger/



This is the first working implementation, focused on \*\*local logging + metrics\*\*:



\- `README\_LOCAL\_LOGGER.txt` – detailed explanation of components and usage

\- `data/`

&nbsp; - `example\_trades.jsonl` – sample TRADE\_EVENT objects

&nbsp; - `trades\_log.jsonl` – main append-only log file (usually ignored by Git)

\- `logger.py`

&nbsp; - core logger; appends validated TRADE\_EVENTs as JSON Lines

\- `trade\_event\_validator.py`

&nbsp; - central validation logic for TRADE\_EVENT objects

\- `simulate\_trades.py`

&nbsp; - generates multiple simulated trades and logs them

\- `metrics\_demo.py`

&nbsp; - computes basic metrics from `.jsonl` logs

\- `metrics\_by\_strategy.py`

&nbsp; - metrics grouped by `strategy\_id` and `account\_id`

\- `generate\_html\_report.py`

&nbsp; - produces a simple HTML report under `reports/index.html`

\- `logger\_service.py`

&nbsp; - local HTTP service exposing `POST /trade\_event` on `http://127.0.0.1:8080`

\- `send\_test\_trade.py`

&nbsp; - small client that sends a TRADE\_EVENT to the local HTTP service

\- `reports/`

&nbsp; - `index.html` – generated local report (open in browser)



---



\## What Works Today (Local Prototype)



On a single machine, TRUEEDGE can:



1\. \*\*Log trades\*\*

&nbsp;  - Manually via `logger.py`

&nbsp;  - In bulk via `simulate\_trades.py`

&nbsp;  - Over HTTP via `logger\_service.py` + `send\_test\_trade.py`



2\. \*\*Compute metrics\*\*

&nbsp;  - Total PnL, total trades, ending equity

&nbsp;  - Simple peak-to-trough max drawdown

&nbsp;  - Wins, losses, win rate

&nbsp;  - Grouped by `strategy\_id` and `account\_id`



3\. \*\*Generate a local HTML report\*\*

&nbsp;  - `python generate\_html\_report.py` produces `reports/index.html` with:

&nbsp;    - overall metrics,

&nbsp;    - per-strategy metrics,

&nbsp;    - per-account metrics.



Everything is currently \*\*file-based\*\* and \*\*local-only\*\*, which keeps it simple and safe.



---



\## Vision (High Level)



TRUEEDGE aims to become a \*\*trust layer\*\* for trading performance:



\- Strategies and accounts emit TRADE\_EVENT objects.

\- TRUEEDGE logs and verifies these events in an append-only fashion.

\- Metrics and reports are computed from real, immutable logs.

\- Over time, this infrastructure can support:

&nbsp; - small funds / prop firms (internal tooling),

&nbsp; - independent traders (SaaS dashboards),

&nbsp; - allocators who need verifiable performance before deploying capital.



This repository is \*\*Phase 0 / Phase 1\*\* of that journey: a clean local prototype

with a clear path toward an open-source core and future backend.



---



\## Local Quickstart



For detailed step-by-step instructions, see:



\- `01\_DOCS/LOCAL\_QUICKSTART.txt`



In short (Windows, from Command Prompt):



```bash

cd %USERPROFILE%\\Desktop\\TRUEEDGE\\02\_CODE\\local\_logger

python logger.py               # log a single demo trade

python simulate\_trades.py      # log multiple simulated trades

python metrics\_demo.py         # see basic metrics

python metrics\_by\_strategy.py  # see metrics grouped by strategy/account

python generate\_html\_report.py # generate reports/index.html

python logger\_service.py       # start local HTTP logger (in one terminal)

python send\_test\_trade.py      # send a demo TRADE\_EVENT over HTTP (in another)



