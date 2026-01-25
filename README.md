# Memecoin Scout Bot

**Automated Solana Memecoin Discovery**

<img width="1880" height="830" alt="Screenshot (188)" src="https://github.com/user-attachments/assets/eea0e16c-c407-4236-8230-aaea68a63c74" />

Memecoin Scout

Real-Time Solana Token Scanner
Built by JA Security | Web3 & DeFi Security Projects

Overview

Memecoin Scout is a real-time scanner for newly launched Solana tokens.
It monitors fresh trading pairs, applies configurable risk filters, scores momentum, and surfaces higher-signal candidates through a lightweight dashboard.

The project is designed as a research and monitoring foundation for live on-chain market data and can be extended toward automated or semi-automated trading strategies.

Key Features

Real-time scanning of new Solana pairs via DexScreener

Risk filtering to remove obvious rugs and low-liquidity tokens

Scoring engine combining liquidity, volume, age, holders, and momentum

Momentum detection for price and volume spikes

SQLite persistence for historical tracking and analysis

Streamlit dashboard for live exploration and filtering

Optional Telegram alerts for higher-scoring tokens

Modular architecture designed for future extensions

Tech Stack

Python 3.11+

Asyncio for concurrent scanning

Streamlit for dashboard UI

SQLite for lightweight persistence

Pandas for data handling

DexScreener API

Telegram Bot API (optional alerts)

Project Structure
memecoin_scout/
├── app/
│   ├── main.py        # Async scanning loop
│   ├── filters.py     # Risk filtering logic
│   ├── scorer.py      # Token scoring engine
│   ├── storagedb.py   # SQLite operations
│   └── alerting/      # Telegram notifications
├── dashboard.py       # Streamlit dashboard
├── utils.py           # Helper functions
├── config.yaml        # Filters, thresholds, API keys
├── requirements.txt   # Python dependencies
└── README.md

How It Works
High-Level Flow
DexScreener → Filters → Scorer → SQLite → Dashboard / Alerts

Process

Continuously polls DexScreener for new Solana pairs

Applies minimum risk criteria (liquidity, holders, age, volume)

Scores remaining tokens on a 0–1 scale using risk and momentum metrics

Stores results in SQLite for tracking and analysis

Displays live data in the Streamlit dashboard

Triggers optional Telegram alerts for higher-scoring tokens

Quick Start
Clone the Repository
git clone https://github.com/JASecurity/memecoin_scout
cd memecoin_scout

Create and Activate Virtual Environment
python -m venv .venv


Windows (PowerShell):

.venv\Scripts\Activate.ps1


Windows (Command Prompt):

.venv\Scripts\activate.bat


Linux / macOS:

source .venv/bin/activate

Install Dependencies
pip install -r requirements.txt

Configuration

Edit config.yaml to match your risk tolerance:

min_liq_usd: 5000
min_vol_5m_usd: 2000
min_score_to_trade: 0.75

telegram_token: "your_bot_token"
telegram_chat_id: "your_chat_id"

paper_mode: true


You can tighten or loosen thresholds depending on how early or conservative you want to be.

Running the Scanner and Dashboard

Open two terminals.

Terminal 1 — Start the Scanner

Windows (PowerShell):

cd memecoin_scout
.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
python app/main.py --live


Windows (Command Prompt):

cd memecoin_scout
.venv\Scripts\activate.bat
set PYTHONPATH=%cd%
python app/main.py --live


Linux / macOS:

cd memecoin_scout
source .venv/bin/activate
export PYTHONPATH=$(pwd)
python app/main.py --live

Terminal 2 — Start the Dashboard
streamlit run dashboard.py

Access the Dashboard

Streamlit will output a local URL, typically:

http://localhost:8501


Open this in your browser to view the dashboard.

Dashboard Features

Live table of recently scanned tokens

Token scores and key metrics

Filters for liquidity, volume, age, and score

Focused views for higher-scoring tokens

Lightweight historical tracking via SQLite

The scanner and dashboard can run continuously to monitor new launches.

Troubleshooting

No new tokens found

Normal during quiet periods

Leave the scanner running

Loosen thresholds in config.yaml

Dashboard does not start

Ensure Streamlit is installed: pip install streamlit

Confirm virtual environment is active

Check port 8501 is free

Run from the project root

Import or module errors

Ensure PYTHONPATH is set

Use Python from .venv

Reinstall dependencies if needed

Roadmap

Planned or potential extensions:

Live trading integration (e.g., Jupiter DEX)

Richer token classification and feature engineering

Multi-chain support (Base, Ethereum, BSC)

Backtesting using SQLite history

Additional alert channels (Discord, Webhooks)

Advanced risk management and position sizing

Why This Project Matters

End-to-end system design (async ingestion → storage → UI)

Practical risk filtering in adversarial markets

Clean operational setup with environments and configuration

Uses real live market data, not static examples

License

MIT — free to fork, extend, and deploy.

Built by JA Security
