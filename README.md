# Memecoin Scout Bot

**Automated Solana Memecoin Discovery**

<img width="1880" height="830" alt="Screenshot (188)" src="https://github.com/user-attachments/assets/eea0e16c-c407-4236-8230-aaea68a63c74" />


Here is the full README with VS Code mentioned and only one set of commands:

Memecoin Scout Bot
Automated Solana Memecoin Discovery

<img width="1880" height="830" alt="Screenshot (188)" src="https://github.com/user-attachments/assets/eea0e16c-c407-4236-8230-aaea68a63c74" />
Memecoin Scout is a real-time scanner for new Solana tokens. It tracks fresh launches, applies risk filters, scores momentum, and surfaces interesting candidates in a simple dashboard. The goal is to provide a solid foundation for building and testing live trading strategies.

Features
Real-time DexScreener scanning for new Solana pairs

Scoring engine combining liquidity, volume, age, holders, and other signals

Risk filters to screen out obvious rugs and low-liquidity tokens

Momentum detection for volume and price spikes

SQLite storage to keep a local history of scanned tokens

Streamlit dashboard for live exploration of tokens and scores

Optional Telegram alerts for higher-scoring tokens

Modular layout that can be extended for auto-trading or multi-chain support

Tech Stack
Python 3.11+
asyncio, Streamlit, SQLite, Pandas
DexScreener API, Telegram Bot API

Project Structure
text
memecoin_scout/
├── app/
│   ├── main.py              # Async scanning loop
│   ├── filters.py           # Risk filtering logic
│   ├── scorer.py            # Token scoring engine
│   ├── storagedb.py         # SQLite operations
│   └── alerting/            # Telegram notifications
├── dashboard.py             # Streamlit dashboard
├── utils.py                 # Helpers / formatting
├── config.yaml              # Filters, thresholds, API keys
├── requirements.txt         # Python dependencies
└── README.md
How It Works
High-level flow:

DexScreener → Filters → Scorer → SQLite → Dashboard / Alerts

The scanner polls new Solana pairs from DexScreener on a loop.

Filters remove tokens that do not meet minimum risk criteria (liquidity, holders, age, etc.).

The scoring engine ranks remaining tokens on a 0–1 scale using momentum and risk metrics.

Data is written to SQLite for later analysis and dashboard use.

The dashboard reads from the database and displays live tokens and scores.

Optional Telegram alerts fire for stronger candidates.

Quick Start
1. Clone and set up
bash
git clone https://github.com/JASecurity/memecoin_scout
cd memecoin_scout
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
2. Configure filters and keys
Edit config.yaml to match your setup and risk appetite:

text
min_liq_usd: 5000
min_vol_5m_usd: 2000
min_score_to_trade: 0.75

telegram_token: "your_bot_token"
telegram_chat_id: "your_chat_id"

paper_mode: true
You can relax or tighten these values depending on how early or conservative you want to be.

Running the Bot and Dashboard
Open the project in VS Code and use split terminals to run both the bot and dashboard side-by-side.

Terminal 1 – Start the bot
Open a terminal in VS Code (Ctrl + `) and run:

powershell
cd "C:\Users\YOUR_USERNAME\Downloads\memecoin_scout\memecoin_scout"
$env:PYTHONPATH = "."
python app/main.py --live
Terminal 2 – Start the dashboard
Split the terminal (Ctrl + Shift + 5) or open a new one, then run:

powershell
cd "C:\Users\YOUR_USERNAME\Downloads\memecoin_scout\memecoin_scout"
& "$env:USERPROFILE\Downloads\memecoin_scout\memecoin_scout\.venv\Scripts\python.exe" -m streamlit run dashboard.py
Access the dashboard
Streamlit will print a local URL, typically:

http://localhost:8501

Open this in your browser to view the dashboard.

Dashboard Overview
Once Streamlit is running, the dashboard provides:

A live table of recently scanned tokens with scores and key metrics

Filters for liquidity, volume, age, and score

A view focused on higher-scoring or flagged tokens

A simple history backed by the SQLite database

The bot and dashboard can be left running together to watch new launches as they appear.

Troubleshooting
Bot prints "No new hidden gem tokens found"

This can be normal during quieter periods.

New tokens launch throughout the day; leave the scanner running.

If you want more candidates, loosen thresholds in config.yaml.

Dashboard does not start

Confirm Streamlit is installed: pip install streamlit.

Ensure the virtual environment is activated.

Check that port 8501 is not already in use.

Make sure you are in the project directory when running the command.

Import or module errors

Confirm PYTHONPATH is set before starting the bot:
$env:PYTHONPATH = "."

Use the Python from .venv when installing and running.

Reinstall dependencies if needed: pip install -r requirements.txt.

Roadmap
Planned or potential extensions:

Live trading integration (for example, via Jupiter DEX)

Smarter token classification using richer feature sets

Support for multiple chains (Base, Ethereum, BSC, etc.)

Backtesting tools over the SQLite history

Additional alert channels such as Discord

More advanced risk and position-sizing logic

Why This Project Matters
This project ties together:

Full-stack thinking across async data collection, storage, and a web UI

Practical risk and market logic tailored to noisy memecoin flows

Operational discipline around environments, configuration, and monitoring

Real, live market data instead of static or toy examples

It is part of a broader set of work under:

JA Security | Web3 & DeFi Security Projects
Hands-on security research, analysis, and tooling focused on Web3, DeFi, and smart contract ecosystems.

License
MIT – free to fork, extend, and deploy.

Star the repository if you find this kind of tooling useful, and feel free to open issues or pull requests with ideas or improvements.

Built by JA Security | Web3 & DeFi Security Projects



