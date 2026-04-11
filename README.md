# Block Boy Security Console

A real-time scanner for newly launched Solana tokens. Detects new trading pairs, applies risk filters, scores momentum and security signals, and surfaces high-confidence candidates through a lightweight live dashboard.

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
Python · Asyncio · Streamlit · SQLite · Pandas
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

> **Note:** The following commands are written for PowerShell. Both terminals must remain open while the system is running.

### Terminal 1 — Start the Scanner

```powershell
cd C:\Users\joeya\Downloads\memecoin_scout\memecoin_scout
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "."
python app/main.py --live
```

**Expected output:**

```
[debug] Found 105 Solana pairs
[debug] 3 live solana pairs accepted after filtering
HIDDEN GEM FOUND: ...
```

### Terminal 2 — Start the Dashboard

```powershell
cd C:\Users\joeya\Downloads\memecoin_scout\memecoin_scout
.\.venv\Scripts\Activate.ps1
streamlit run app/dashboard.py
```

Streamlit will output a local URL such as `http://localhost:8501`. Open this address in a browser to view the live dashboard.

---

## Configuration

### `config.yaml`

- Liquidity thresholds
- Holder requirements
- Scan intervals
- Risk score thresholds
- Telegram alert settings

### `.env` Environment Variables

```
SOLANA_RPC_URL=your_rpc_url
TELEGRAM_BOT_TOKEN=your_telegram_token
TELEGRAM_CHAT_ID=your_chat_id
```

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
