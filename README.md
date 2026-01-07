# Memecoin Scout Bot

**Automated Solana Memecoin Discovery**

<img width="1880" height="830" alt="Screenshot (188)" src="https://github.com/user-attachments/assets/eea0e16c-c407-4236-8230-aaea68a63c74" />


Real-time token scanner that identifies promising new memecoins on Solana, applies risk filters, scores momentum, and visualizes everything via an interactive dashboard. Built as a modular foundation for live trading strategies.

## 🚀 Features

## 🚀 Features

- **Real-time DexScreener Scanning**: Fetches new Solana token pairs every 3 minutes
- **Advanced Scoring Engine**: Combines liquidity, volume, holders, and social signals
- **Hard Risk Filters**: Min $3K liquidity, 5+ holders, 50%+ LP lock, low taxes
- **Momentum Spike Detection**: Identifies volume/price surges for early alerts
- **SQLite Persistence**: Stores all token data for analysis
- **Streamlit Dashboard**: Live views of scanned tokens and alerts
- **Telegram Alerts**: Instant notifications for qualifying tokens
- **Modular Architecture**: Easy to extend for auto-trading or multi-chain

## 🏗️ Tech Stack

Python 3.11+ | asyncio | Streamlit | SQLite | Pandas
DexScreener APIs | Telegram Bot API

## 📁 Project Structure
memecoin_scout/
├── app/
│ ├── main.py # Async scanning loop
│ ├── filters.py # Risk filtering logic
│ ├── scorer.py # Token scoring engine
│ ├── storagedb.py # SQLite operations
│ └── alerting/ # Telegram notifications
├── dashboard.py # Streamlit visualization
├── utils.py # Data formatting
├── config.yaml # Filters & API keys
├── requirements.txt # Dependencies
└── README.md


text

## 🎯 How It Works

DexScreener → Filter (liq/vol/holders) → Score (momentum/risk) → SQLite → Dashboard/Alerts

1. **Scanner** polls new Solana pairs
2. **Filters** reject rugs/low-liq tokens
3. **Scorer** ranks survivors (0-1.0 scale)
4. **Momentum Detector** flags volume spikes
5. **Telegram** sends instant alerts
6. **Dashboard** shows real-time insights

## 🛠️ Quick Start

### Prerequisites
git clone <repo>
cd memecoin_scout
python -m venv .venv
.venv\Scripts\activate # Windows
pip install -r requirements.txt


### 1. Run Live Bot (Terminal 1)
& ".venv\Scripts\python.exe" -m app.main --live


### 2. Open Dashboard (Terminal 2)
& ".venv\Scripts\python.exe" -m streamlit run dashboard.py



## ⚙️ Configuration

Edit `config.yaml`:
min_liq_usd: 5000
min_vol_5m_usd: 2000
min_score_to_trade: 0.75
telegram_token: "your_bot_token"
telegram_chat_id: "your_chat_id"
paper_mode: true


## 📊 Dashboard Screenshots

**Latest Tokens Table**
| Rank | Symbol | Score | Liq USD | Vol 1H | Holders | LP Lock |
|------|--------|-------|---------|--------|---------|---------|
| 1    | $MOON  | 0.92  | $12.5K  | $8.2K  | 245     | 87%     |

**Trade Log & Positions**

## 🔮 Future Roadmap

- [ ] Live Jupiter DEX trading
- [ ] AI-powered token classification
- [ ] Multi-chain (Base, ETH, BSC)
- [ ] Backtesting engine
- [ ] Discord webhooks
- [ ] Advanced risk models

💼 Why Employers Should Care
This project demonstrates:

Full-Stack Development: APIs, databases, web UIs, async processing

Financial Engineering: Risk management, position sizing, strategy backtesting

DevOps: Virtualenvs, config management, logging, monitoring

Real-World Data: Live crypto APIs, high-frequency polling

Production-Ready: Error handling, persistence, alerting, dashboards

10+ years construction management → Cybersecurity → Now algorithmic trading

Transitioning from foundation specialist/crew leader to building production trading systems. Self-taught Python, Solana ecosystem, and quant strategies.


## 📄 License
MIT - Free to fork, extend, deploy.

---

⭐ **Star if you find memecoin hunting interesting!**  
💬 **Issues/PRs welcome**  
🔗 **Demo video coming soon**

---

*Built by InvestaDad - Aspiring Cybersecurity Analyst | Google Cybersecurity Cert | Future Smart Contract Auditor*

