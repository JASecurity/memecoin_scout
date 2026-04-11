# Block Boy Security Console

<img width="1916" height="908" alt="Screenshot 2026-04-10 200931" src="https://github.com/user-attachments/assets/1fc4781b-9b6b-4a5e-95a2-7249afdbb6b8" />

A real-time scanner for newly launched Solana tokens. Detects new trading pairs, applies risk filters, scores momentum and security signals, and surfaces high-confidence candidates through an immersive retro live dashboard.

Designed as a Solana-focused research and monitoring system, it provides live on-chain market insights and serves as a foundation for automation, trading strategy development, and security research.

---

## Features

### Solana Token Scanning

- Real-time detection of new Solana pairs via DexScreener, Raydium, Orca, and Pump.fun
- Scans approximately 96 unique token pairs every 60 to 90 seconds
- Liquidity and risk-based filtering pipeline
- Momentum scoring across liquidity, volume, age, and holder count
- Duplicate tracking to prevent redundant processing

### Data Management and Alerts

- SQLite database for persistent historical analysis
- Streamlit dashboard for live token monitoring
- Optional Telegram alerts for high-scoring token candidates
- Modular and extensible architecture

---

## Tech Stack

```
Python · Asyncio · Streamlit · SQLite · Pandas · Plotly
DexScreener API · Solana RPC · Telegram Bot API
```

---

## Architecture

```
DexScreener → Filters → Scoring → SQLite → Dashboard / Alerts
```

The scanner continuously ingests live Solana market data, applies risk filters, scores tokens against configurable thresholds, persists results to a local database, and exposes them via a live web dashboard.

---

## Filters and Thresholds

The default filter values are intentionally strict to minimize noise and surface only high-confidence candidates. Depending on your risk tolerance and scanning goals, you may want to loosen these thresholds — for example, lowering the minimum holder count or extending the token age window. All values are adjustable via `config.yaml`.

| Filter | Threshold |
| --- | --- |
| Minimum Liquidity | $1,500 |
| Maximum Liquidity | $1,000,000 |
| Minimum Holders | 10 |
| Token Age | 5 to 1,440 minutes |
| Price Range | Low-priced memecoins |
| Tax / Honeypot Detection | Enabled |

---

## Installation and Setup (Windows)

> **Important:** Run each command one at a time. Copy one line, hit Enter, wait for it to finish, then do the next. Never combine commands on the same line.

---

### Step 1 — Clone the repo

Open PowerShell and run these one at a time:

```powershell
git clone https://github.com/joseph-alexan/sol-token-scanner.git
```

```powershell
cd sol-token-scanner
```

---

### Step 2 — Create a virtual environment

```powershell
python -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

You should see `(.venv)` appear at the start of your terminal line. That means it worked.

> **If Activate.ps1 is blocked**, run this first then try again:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

---

### Step 3 — Install dependencies

```powershell
pip install -r memecoin_scout/requirements.txt
```

```powershell
pip install plotly
```

---

### Step 4 — Set up your environment variables

Inside the `memecoin_scout` folder, create a file called `.env` and add the following:

```
SOLANA_RPC_URL=your_rpc_url
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

Telegram alerts are optional. The scanner will run without them.

---

## Running the Project

You need **two terminals open at the same time**. Open Terminal 1, start the scanner, then open a second terminal and start the dashboard.

---

### Terminal 1 — Start the Scanner

```powershell
cd sol-token-scanner/memecoin_scout
```

```powershell
$env:PYTHONPATH = "."
```

```powershell
python app/main.py --live
```

**Expected output:**

```
[live] Memecoin Scout + Momentum started...
[info] Fetching new tokens from DexScreener...
[debug] Found 105 Solana pairs
[debug] 3 live solana pairs accepted after filtering
HIDDEN GEM FOUND: ...
```

Leave this terminal running. Do not close it.

---

### Terminal 2 — Start the Dashboard

Open a new terminal window, then run these one at a time:

```powershell
cd sol-token-scanner
```

```powershell
.\.venv\Scripts\Activate.ps1
```

```powershell
streamlit run memecoin_scout/dashboard.py
```

Then open your browser and go to:

```
http://localhost:8501
```

The dashboard will auto-refresh as the scanner finds new tokens.

---

## Configuration

### `config.yaml`

- Liquidity thresholds
- Holder requirements
- Scan intervals
- Risk score thresholds
- Telegram alert settings

---

## Why This Project

- Async system design for real-time, low-latency monitoring
- Solana-native token discovery and on-chain analysis
- Practical risk filtering in adversarial memecoin markets
- Clean separation of concerns: scanning, scoring, storage, and UI
- Demonstrates applied Web3 security and data engineering skills
- Foundation for automated Solana trading and alerting strategies

---

## Roadmap

**Current Phase: Risk Scoring Optimization**

- Reduce false positives on new Solana launches
- Improve liquidity and holder-based heuristics
- Advanced honeypot and rug-risk detection

**Next Phase: Enhanced Web Dashboard**

- Expanded real-time visualizations
- Historical trend analysis
- Token comparison tools

**Future Enhancements**

- Solana wallet tracking and behavioral analysis
- Automated alert optimization
- DEX aggregator integration
- Strategy backtesting on historical Solana data

---

## License

MIT License

---

Built by Joseph Alexan | Web3 and DeFi Security Projects
