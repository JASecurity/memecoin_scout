import os
from pathlib import Path
from datetime import datetime, timezone, timedelta
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import time

# ─── PAGE CONFIG ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🕹️ Block Boy Security Console",
    page_icon="🕹️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── PATHS ────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT.parent / "token_logs.csv"
MOMENTUM_FILE = ROOT.parent / "momentum_logs.csv"

# ─── MASTER CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&family=VT323:wght@400&family=Silkscreen:wght@400;700&display=swap');

/* ── RESET & BASE ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --gb-dark:    #0f380f;
  --gb-mid:     #306230;
  --gb-light:   #8bac0f;
  --gb-pale:    #9bbc0f;
  --gb-shell:   #c8b89a;
  --gb-purple:  #6b4d9e;
  --gb-red:     #d92b3a;
  --gb-amber:   #f5a623;
  --gb-cyan:    #14f195;
  --gb-sol:     #9945ff;
  --pixel:      2px;
  --font-main:  'Press Start 2P', monospace;
  --font-vt:    'VT323', monospace;
  --font-silk:  'Silkscreen', monospace;
}

/* ── SCANLINE OVERLAY ── */
.stApp::before {
  content: '';
  position: fixed; inset: 0;
  background: repeating-linear-gradient(
    0deg,
    transparent,
    transparent 2px,
    rgba(0,0,0,0.04) 2px,
    rgba(0,0,0,0.04) 4px
  );
  pointer-events: none;
  z-index: 9999;
  mix-blend-mode: multiply;
}

/* ── BODY ── */
.stApp {
  background-color: #0a0a12 !important;
  background-image:
    radial-gradient(ellipse 80% 60% at 50% -10%, rgba(153,69,255,0.18) 0%, transparent 70%),
    radial-gradient(ellipse 50% 40% at 80% 110%, rgba(20,241,149,0.10) 0%, transparent 60%),
    repeating-linear-gradient(
      90deg,
      transparent,
      transparent 59px,
      rgba(155,188,15,0.03) 59px,
      rgba(155,188,15,0.03) 60px
    ),
    repeating-linear-gradient(
      0deg,
      transparent,
      transparent 59px,
      rgba(155,188,15,0.03) 59px,
      rgba(155,188,15,0.03) 60px
    );
  color: var(--gb-pale) !important;
  font-family: var(--font-main) !important;
}

.main .block-container {
  padding: 1.5rem 2rem 3rem !important;
  max-width: 100% !important;
}

/* ── HEADER HERO ── */
.console-header {
  position: relative;
  background: linear-gradient(135deg, #0d0d1a 0%, #1a0d2e 50%, #0d1a0d 100%);
  border: 3px solid var(--gb-pale);
  box-shadow:
    0 0 0 1px var(--gb-mid),
    0 0 20px rgba(155,188,15,0.3),
    0 0 60px rgba(153,69,255,0.15),
    inset 0 1px 0 rgba(155,188,15,0.2);
  padding: 28px 36px;
  margin-bottom: 24px;
  overflow: hidden;
}

.console-header::before {
  content: '';
  position: absolute; inset: 0;
  background: repeating-linear-gradient(
    -45deg,
    transparent,
    transparent 10px,
    rgba(155,188,15,0.015) 10px,
    rgba(155,188,15,0.015) 11px
  );
}

.console-header-inner {
  position: relative; z-index: 1;
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 16px;
}

.console-logo {
  font-family: var(--font-main);
  font-size: clamp(12px, 2vw, 18px);
  color: var(--gb-pale);
  text-shadow:
    0 0 8px var(--gb-pale),
    0 0 20px rgba(155,188,15,0.5),
    2px 2px 0 var(--gb-dark);
  letter-spacing: 2px;
  line-height: 1.6;
}

.console-logo span {
  color: var(--gb-cyan);
  text-shadow: 0 0 10px var(--gb-cyan), 0 0 25px rgba(20,241,149,0.4);
}

.live-badge {
  display: inline-flex; align-items: center; gap: 8px;
  background: rgba(15,56,15,0.8);
  border: 2px solid var(--gb-mid);
  padding: 8px 14px;
  font-family: var(--font-silk);
  font-size: 13px;
  color: var(--gb-pale);
}

.live-dot {
  width: 8px; height: 8px;
  background: var(--gb-pale);
  border-radius: 50%;
  animation: pulse-dot 1s steps(1) infinite;
}

@keyframes pulse-dot {
  0%, 100% { opacity: 1; }
  50%       { opacity: 0; }
}

/* ── PIXEL STAT CARDS ── */
.stat-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.stat-card {
  background: linear-gradient(145deg, #111820 0%, #0d1208 100%);
  border: 2px solid var(--gb-mid);
  padding: 16px;
  position: relative;
  transition: border-color 0.15s, box-shadow 0.15s, transform 0.1s;
  cursor: default;
}

.stat-card::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, transparent, var(--gb-pale), transparent);
  opacity: 0;
  transition: opacity 0.2s;
}

.stat-card:hover {
  border-color: var(--gb-pale);
  box-shadow: 0 0 16px rgba(155,188,15,0.3), 0 0 4px rgba(155,188,15,0.6);
  transform: translateY(-2px);
}

.stat-card:hover::before { opacity: 1; }

.stat-label {
  font-family: var(--font-silk);
  font-size: 10px;
  color: var(--gb-mid);
  letter-spacing: 1px;
  margin-bottom: 8px;
  text-transform: uppercase;
}

.stat-value {
  font-family: var(--font-vt);
  font-size: 36px;
  color: var(--gb-pale);
  text-shadow: 0 0 8px rgba(155,188,15,0.5);
  line-height: 1;
}

.stat-value.danger  { color: var(--gb-red);   text-shadow: 0 0 8px rgba(217,43,58,0.6); }
.stat-value.warning { color: var(--gb-amber);  text-shadow: 0 0 8px rgba(245,166,35,0.6); }
.stat-value.success { color: var(--gb-cyan);   text-shadow: 0 0 8px rgba(20,241,149,0.5); }
.stat-value.sol     { color: var(--gb-sol);    text-shadow: 0 0 8px rgba(153,69,255,0.6); }

/* ── SECTION HEADERS ── */
.section-header {
  display: flex; align-items: center; gap: 12px;
  margin: 28px 0 16px;
}

.section-title {
  font-family: var(--font-main);
  font-size: 11px;
  color: var(--gb-pale);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.section-line {
  flex: 1;
  height: 1px;
  background: linear-gradient(90deg, var(--gb-mid), transparent);
}

/* ── TOKEN CARDS ── */
.token-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}

.token-card {
  background: #0d1208;
  border: 2px solid var(--gb-mid);
  padding: 0;
  position: relative;
  overflow: hidden;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.15s;
  cursor: pointer;
}

.token-card:hover {
  border-color: var(--gb-pale);
  box-shadow: 0 0 20px rgba(155,188,15,0.25), 0 6px 20px rgba(0,0,0,0.4);
  transform: translateY(-3px);
}

.token-card-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 12px 14px 10px;
  border-bottom: 1px solid var(--gb-dark);
  background: rgba(48,98,48,0.12);
}

.token-symbol {
  font-family: var(--font-main);
  font-size: 11px;
  color: var(--gb-pale);
}

.threat-badge {
  font-family: var(--font-silk);
  font-size: 10px;
  padding: 3px 8px;
  border: 1px solid currentColor;
}

.threat-critical { color: #ff3355; border-color: #ff3355; background: rgba(255,51,85,0.1); }
.threat-high     { color: var(--gb-amber); border-color: var(--gb-amber); background: rgba(245,166,35,0.1); }
.threat-medium   { color: var(--gb-sol);   border-color: var(--gb-sol);   background: rgba(153,69,255,0.1); }
.threat-low      { color: var(--gb-pale);  border-color: var(--gb-mid);   background: rgba(155,188,15,0.05); }

.token-card-body {
  padding: 12px 14px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}

.token-stat { }

.token-stat-label {
  font-family: var(--font-silk);
  font-size: 9px;
  color: rgba(155,188,15,0.45);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.token-stat-val {
  font-family: var(--font-vt);
  font-size: 20px;
  color: var(--gb-pale);
  line-height: 1.1;
}

.token-card-footer {
  padding: 8px 14px;
  border-top: 1px solid var(--gb-dark);
  display: flex; gap: 6px;
}

.px-btn {
  flex: 1;
  background: rgba(48,98,48,0.3);
  border: 1px solid var(--gb-mid);
  color: var(--gb-pale);
  font-family: var(--font-silk);
  font-size: 9px;
  padding: 5px 0;
  text-align: center;
  text-decoration: none;
  display: block;
  transition: background 0.15s, border-color 0.15s;
  cursor: pointer;
}

.px-btn:hover {
  background: rgba(155,188,15,0.15);
  border-color: var(--gb-pale);
  color: var(--gb-pale);
  text-decoration: none;
}

/* Score bar */
.score-bar-wrap {
  grid-column: 1 / -1;
  margin-top: 4px;
}

.score-bar-track {
  height: 6px;
  background: var(--gb-dark);
  border: 1px solid var(--gb-mid);
  position: relative;
  overflow: hidden;
}

.score-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--gb-mid), var(--gb-pale));
  transition: width 0.4s ease;
  position: relative;
}

.score-bar-fill::after {
  content: '';
  position: absolute; right: 0; top: 0; bottom: 0;
  width: 3px;
  background: white;
  opacity: 0.8;
  box-shadow: 0 0 6px var(--gb-pale);
}

/* ── EMPTY STATE ── */
.empty-console {
  border: 2px solid var(--gb-mid);
  padding: 48px 24px;
  text-align: center;
  background: #0d1208;
}

.empty-console-icon {
  font-size: 48px;
  margin-bottom: 20px;
  animation: float 3s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50%       { transform: translateY(-8px); }
}

.empty-console-title {
  font-family: var(--font-main);
  font-size: 12px;
  color: var(--gb-pale);
  margin-bottom: 12px;
}

.empty-console-sub {
  font-family: var(--font-vt);
  font-size: 20px;
  color: var(--gb-mid);
}

/* ── SIDEBAR ── */
section[data-testid="stSidebar"] {
  background: #090e09 !important;
  border-right: 2px solid var(--gb-mid) !important;
}

section[data-testid="stSidebar"] > div {
  padding-top: 1rem;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div {
  color: var(--gb-pale) !important;
  font-family: var(--font-silk) !important;
}

section[data-testid="stSidebar"] .stMarkdown p {
  font-size: 11px !important;
}

section[data-testid="stSidebar"] .stSlider > div > div > div {
  background: var(--gb-mid) !important;
}

/* ── INPUTS ── */
.stTextInput input,
.stNumberInput input {
  background: #0d1208 !important;
  border: 2px solid var(--gb-mid) !important;
  color: var(--gb-pale) !important;
  font-family: var(--font-silk) !important;
  font-size: 12px !important;
  border-radius: 0 !important;
}

.stTextInput input:focus,
.stNumberInput input:focus {
  border-color: var(--gb-pale) !important;
  box-shadow: 0 0 8px rgba(155,188,15,0.3) !important;
}

/* ── BUTTONS ── */
.stButton > button {
  background: var(--gb-dark) !important;
  border: 2px solid var(--gb-mid) !important;
  color: var(--gb-pale) !important;
  font-family: var(--font-silk) !important;
  font-size: 11px !important;
  border-radius: 0 !important;
  transition: all 0.15s !important;
  box-shadow: 3px 3px 0 var(--gb-dark) !important;
}

.stButton > button:hover {
  background: rgba(155,188,15,0.12) !important;
  border-color: var(--gb-pale) !important;
  box-shadow: 2px 2px 0 var(--gb-dark), 0 0 12px rgba(155,188,15,0.25) !important;
  transform: translate(1px, 1px) !important;
}

/* ── MULTISELECT ── */
.stMultiSelect [data-baseweb="tag"] {
  background: var(--gb-dark) !important;
  border: 1px solid var(--gb-mid) !important;
  border-radius: 0 !important;
}

/* ── CHECKBOX ── */
.stCheckbox label span { font-family: var(--font-silk) !important; font-size: 11px !important; }

/* ── DIVIDER ── */
hr { border-color: var(--gb-mid) !important; border-width: 1px !important; margin: 16px 0 !important; }

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--gb-dark); }
::-webkit-scrollbar-thumb { background: var(--gb-mid); }
::-webkit-scrollbar-thumb:hover { background: var(--gb-pale); }

/* ── ALERT TICKER ── */
.ticker-wrap {
  overflow: hidden;
  border: 1px solid var(--gb-mid);
  background: #0a0e0a;
  padding: 6px 0;
  margin-bottom: 20px;
}

.ticker-inner {
  display: inline-block;
  white-space: nowrap;
  animation: ticker 28s linear infinite;
  font-family: var(--font-vt);
  font-size: 18px;
  color: var(--gb-light);
}

@keyframes ticker {
  0%   { transform: translateX(100vw); }
  100% { transform: translateX(-100%); }
}

/* ── PROGRESS / MOMENTUM BARS ── */
.momentum-row {
  display: flex; align-items: center; gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid rgba(48,98,48,0.3);
}

.momentum-symbol {
  font-family: var(--font-main);
  font-size: 9px;
  color: var(--gb-pale);
  width: 70px; flex-shrink: 0;
}

.momentum-track {
  flex: 1;
  height: 8px;
  background: var(--gb-dark);
  border: 1px solid rgba(48,98,48,0.4);
  position: relative;
}

.momentum-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--gb-mid), var(--gb-cyan));
  box-shadow: 0 0 6px rgba(20,241,149,0.4);
}

.momentum-val {
  font-family: var(--font-vt);
  font-size: 18px;
  color: var(--gb-pale);
  width: 55px; text-align: right; flex-shrink: 0;
}

/* ── ALERT BOX ── */
.alert-box {
  border: 2px solid;
  padding: 14px 16px;
  margin-bottom: 10px;
  display: flex; align-items: flex-start; gap: 12px;
  position: relative;
  overflow: hidden;
}

.alert-box::before {
  content: '';
  position: absolute; inset: 0;
  background: currentColor;
  opacity: 0.04;
}

.alert-box.critical { border-color: #ff3355; color: #ff3355; }
.alert-box.high     { border-color: var(--gb-amber); color: var(--gb-amber); }
.alert-box.info     { border-color: var(--gb-mid); color: var(--gb-pale); }

.alert-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }

.alert-content { font-family: var(--font-silk); font-size: 10px; line-height: 1.8; }

.alert-title { font-size: 11px; margin-bottom: 4px; }

/* ── FOOTER ── */
.console-footer {
  margin-top: 40px;
  border-top: 1px solid var(--gb-mid);
  padding-top: 16px;
  display: flex; align-items: center; justify-content: space-between;
  flex-wrap: wrap; gap: 12px;
}

.footer-text {
  font-family: var(--font-silk);
  font-size: 9px;
  color: rgba(155,188,15,0.4);
  letter-spacing: 1px;
}

/* ── OVERRIDES for Streamlit native elements ── */
div[data-testid="metric-container"] {
  background: #0d1208 !important;
  border: 2px solid var(--gb-mid) !important;
  padding: 12px !important;
  border-radius: 0 !important;
}

[data-testid="stMetricLabel"] {
  font-family: var(--font-silk) !important;
  font-size: 9px !important;
  color: var(--gb-mid) !important;
}

[data-testid="stMetricValue"] {
  font-family: var(--font-vt) !important;
  font-size: 32px !important;
  color: var(--gb-pale) !important;
}

/* ── PIXEL BORDER HELPER ── */
.pixel-box {
  border: 2px solid var(--gb-mid);
  background: #0d1208;
  padding: 16px;
}

/* Select boxes */
.stSelectbox [data-baseweb="select"] > div {
  background: #0d1208 !important;
  border: 2px solid var(--gb-mid) !important;
  border-radius: 0 !important;
  font-family: var(--font-silk) !important;
  color: var(--gb-pale) !important;
}

</style>
""", unsafe_allow_html=True)

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def threat_class(score):
    if score >= 8: return ("CRITICAL", "threat-critical")
    if score >= 7: return ("HIGH",     "threat-high")
    if score >= 6: return ("MEDIUM",   "threat-medium")
    return ("LOW", "threat-low")

def stat_color(label, val):
    if "SCORE" in label.upper() and isinstance(val, (int, float)):
        if val >= 8: return "danger"
        if val >= 6: return "warning"
        return "success"
    return ""

# ─── DATA LOAD ────────────────────────────────────────────────────────────────
@st.cache_data(ttl=15)
def load_token_data():
    if not LOG_FILE.exists():
        return pd.DataFrame()
    df = pd.read_csv(LOG_FILE)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

@st.cache_data(ttl=15)
def load_momentum_data():
    if not MOMENTUM_FILE.exists():
        return pd.DataFrame()
    df = pd.read_csv(MOMENTUM_FILE)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# ─── SIDEBAR ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:12px 0 20px; border-bottom:1px solid var(--gb-mid); margin-bottom:20px;">
      <div style="font-family:var(--font-main);font-size:10px;color:var(--gb-pale);letter-spacing:2px;margin-bottom:6px;">🕹️ BLOCK BOY</div>
      <div style="font-family:var(--font-silk);font-size:11px;color:var(--gb-mid);">SECURITY CONSOLE v2.0</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-family:var(--font-main);font-size:9px;color:var(--gb-pale);letter-spacing:1px;margin-bottom:10px;">⚙ SCAN CONFIG</div>', unsafe_allow_html=True)
    auto_refresh = st.slider("REFRESH RATE (SEC)", 5, 60, 15)
    min_score    = st.slider("MIN THREAT SCORE", 0, 10, 6)
    min_holders  = st.number_input("MIN HOLDERS", 0, 1000, 0)

    st.markdown("---")
    st.markdown('<div style="font-family:var(--font-main);font-size:9px;color:var(--gb-pale);letter-spacing:1px;margin-bottom:10px;">🎯 FILTERS</div>', unsafe_allow_html=True)
    require_momentum = st.checkbox("MOMENTUM > +20%", False)
    show_today_only  = st.checkbox("TODAY ONLY", False)
    search_symbol    = st.text_input("SEARCH TOKEN", "").upper()
    chains           = st.multiselect("CHAINS", ["solana", "ethereum", "bsc"], default=["solana"])

    st.markdown("---")
    st.markdown(f"""
    <div style="font-family:var(--font-silk);font-size:10px;color:var(--gb-pale);">
      <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;">
        <span style="width:8px;height:8px;background:var(--gb-pale);display:inline-block;animation:pulse-dot 1s steps(1) infinite;"></span>
        SCANNER: ACTIVE
      </div>
      <div style="color:var(--gb-mid);font-size:9px;">REFRESH: {auto_refresh}s INTERVAL</div>
      <div style="color:var(--gb-mid);font-size:9px;margin-top:4px;">CHAIN: SOLANA MAINNET</div>
    </div>
    """, unsafe_allow_html=True)

    env_ok = Path(".env").exists()
    color  = "var(--gb-pale)" if env_ok else "var(--gb-red)"
    label  = "API KEYS: SECURED ✓" if env_ok else "NO .ENV FOUND ✗"
    st.markdown(f"""
    <div style="margin-top:16px;border:1px solid {color};padding:8px 10px;font-family:var(--font-silk);font-size:9px;color:{color};">
      {label}
    </div>
    """, unsafe_allow_html=True)

# ─── LOAD & FILTER ────────────────────────────────────────────────────────────
tokens_df   = load_token_data()
momentum_df = load_momentum_data()

if not tokens_df.empty:
    if 'score'   in tokens_df.columns: tokens_df = tokens_df[tokens_df['score'] >= min_score]
    if min_holders > 0 and 'holders' in tokens_df.columns:
        tokens_df = tokens_df[tokens_df['holders'] >= min_holders]
    if search_symbol and 'symbol' in tokens_df.columns:
        tokens_df = tokens_df[tokens_df['symbol'].str.contains(search_symbol, case=False, na=False)]
    if 'chain' in tokens_df.columns:
        tokens_df = tokens_df[tokens_df['chain'].isin(chains)]
    if show_today_only and 'timestamp' in tokens_df.columns:
        today     = datetime.now(timezone.utc).date()
        tokens_df = tokens_df[tokens_df['timestamp'].dt.date == today]

# ─── HEADER ───────────────────────────────────────────────────────────────────
now_str   = datetime.now(timezone.utc).strftime('%H:%M:%S UTC')
scan_count= len(tokens_df) if not tokens_df.empty else 0

st.markdown(f"""
<div class="console-header">
  <div class="console-header-inner">
    <div>
      <div class="console-logo">🔒 BLOCK BOY<br><span>SECURITY CONSOLE</span></div>
      <div style="font-family:var(--font-silk);font-size:10px;color:var(--gb-mid);margin-top:8px;letter-spacing:1px;">
        SOLANA BLOCKCHAIN THREAT INTELLIGENCE SYSTEM
      </div>
    </div>
    <div style="display:flex;flex-direction:column;gap:8px;align-items:flex-end;">
      <div class="live-badge"><span class="live-dot"></span> LIVE SCAN</div>
      <div style="font-family:var(--font-vt);font-size:22px;color:var(--gb-mid);">{now_str}</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── NEWS TICKER ──────────────────────────────────────────────────────────────
ticker_items = []
if not tokens_df.empty and 'symbol' in tokens_df.columns:
    for _, row in tokens_df.head(6).iterrows():
        sym   = row.get('symbol', '???')
        score = row.get('score', 0)
        liq   = row.get('liquidity_usd', 0)
        ticker_items.append(f"  ⚡ ${sym} THREAT:{score:.1f}/10 LIQ:${liq:,.0f}  ∙∙∙")
else:
    ticker_items = ["  ⚡ AWAITING DATA STREAM  ∙∙∙  SCANNER ACTIVE  ∙∙∙  INITIALIZING THREAT DETECTION  ∙∙∙"]

st.markdown(f"""
<div class="ticker-wrap">
  <span class="ticker-inner">{''.join(ticker_items * 3)}</span>
</div>
""", unsafe_allow_html=True)

# ─── STAT CARDS ───────────────────────────────────────────────────────────────
total = len(tokens_df) if not tokens_df.empty else 0
avg_h = int(tokens_df['holders'].mean()) if not tokens_df.empty and 'holders' in tokens_df.columns and len(tokens_df) else 0
flagged = int((tokens_df['score'] >= 8).sum()) if not tokens_df.empty and 'score' in tokens_df.columns else 0
mint_pct = 0
if not tokens_df.empty and 'mint_safe' in tokens_df.columns and len(tokens_df):
    mint_pct = int(tokens_df['mint_safe'].sum() / len(tokens_df) * 100)

avg_score_cls  = "danger" if flagged > 0 else "success"
mint_cls       = "success" if mint_pct >= 70 else ("warning" if mint_pct >= 40 else "danger")

st.markdown(f"""
<div class="stat-row">
  <div class="stat-card">
    <div class="stat-label">TOKENS SCANNED</div>
    <div class="stat-value sol">{total}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">AVG HOLDERS</div>
    <div class="stat-value">{avg_h:,}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">CRITICAL FLAGS</div>
    <div class="stat-value {avg_score_cls}">{flagged}</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">MINT SECURED</div>
    <div class="stat-value {mint_cls}">{mint_pct}%</div>
  </div>
  <div class="stat-card">
    <div class="stat-label">SCAN RATE</div>
    <div class="stat-value">{auto_refresh}s</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── DETECTED TOKENS ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header">
  <div class="section-title">🎯 DETECTED TOKENS</div>
  <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

if tokens_df.empty:
    st.markdown("""
    <div class="empty-console">
      <div class="empty-console-icon">📡</div>
      <div class="empty-console-title">NO TOKENS DETECTED</div>
      <div class="empty-console-sub">AWAITING DATA STREAM — ENSURE SCANNER IS ACTIVE</div>
    </div>
    """, unsafe_allow_html=True)
else:
    display_df = tokens_df.sort_values('score', ascending=False).head(12) if 'score' in tokens_df.columns else tokens_df.head(12)
    cards_html = '<div class="token-grid">'

    for _, row in display_df.iterrows():
        symbol  = row.get('symbol', '???')
        score   = float(row.get('score', 0))
        liq     = float(row.get('liquidity_usd', 0))
        holders = int(row.get('holders', 0))
        age_min = float(row.get('age_minutes', 0))
        price   = float(row.get('price_usd', 0))
        address = str(row.get('address', ''))
        age_d   = age_min / 1440

        tlabel, tclass = threat_class(score)
        score_pct      = min(score / 10 * 100, 100)
        dex_url        = f"https://dexscreener.com/solana/{address}" if address else "#"
        cg_url         = f"https://www.coingecko.com/en/coins/{symbol.lower()}"
        tw_url         = f"https://twitter.com/search?q=${symbol}"
        addr_short     = (address[:12] + "...") if len(address) > 12 else address

        cards_html += f"""
        <div class="token-card">
          <div class="token-card-header">
            <span class="token-symbol">$ {symbol}</span>
            <span class="threat-badge {tclass}">{tlabel}</span>
          </div>
          <div class="token-card-body">
            <div class="token-stat">
              <div class="token-stat-label">THREAT SCORE</div>
              <div class="token-stat-val">{score:.1f}<span style="font-size:13px;color:var(--gb-mid)">/10</span></div>
            </div>
            <div class="token-stat">
              <div class="token-stat-label">LIQUIDITY</div>
              <div class="token-stat-val">${liq:,.0f}</div>
            </div>
            <div class="token-stat">
              <div class="token-stat-label">HOLDERS</div>
              <div class="token-stat-val">{holders if holders > 0 else 'N/A'}</div>
            </div>
            <div class="token-stat">
              <div class="token-stat-label">AGE</div>
              <div class="token-stat-val">{age_d:.1f}<span style="font-size:13px;color:var(--gb-mid)">d</span></div>
            </div>
            <div class="token-stat">
              <div class="token-stat-label">PRICE USD</div>
              <div class="token-stat-val" style="font-size:15px">${price:.8f}</div>
            </div>
            <div class="token-stat">
              <div class="token-stat-label">ADDRESS</div>
              <div class="token-stat-val" style="font-size:13px;color:var(--gb-mid)">{addr_short}</div>
            </div>
            <div class="score-bar-wrap">
              <div class="score-bar-track">
                <div class="score-bar-fill" style="width:{score_pct:.0f}%"></div>
              </div>
            </div>
          </div>
          <div class="token-card-footer">
            <a class="px-btn" href="{dex_url}" target="_blank">DEX</a>
            <a class="px-btn" href="{cg_url}" target="_blank">GECKO</a>
            <a class="px-btn" href="{tw_url}" target="_blank">TWITTER</a>
          </div>
        </div>"""

    cards_html += '</div>'
    st.markdown(cards_html, unsafe_allow_html=True)

# ─── MOMENTUM ANALYSIS ────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header" style="margin-top:32px;">
  <div class="section-title">📊 MOMENTUM ANALYSIS</div>
  <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([3, 2])

with col_left:
    if not tokens_df.empty and 'score' in tokens_df.columns and len(tokens_df) >= 2:
        top5 = tokens_df.nlargest(5, 'score')
        bars_html = '<div class="pixel-box">'
        for _, row in top5.iterrows():
            sym   = row.get('symbol', '???')
            score = float(row.get('score', 0))
            pct   = min(score / 10 * 100, 100)
            bars_html += f"""
            <div class="momentum-row">
              <div class="momentum-symbol">${sym}</div>
              <div class="momentum-track">
                <div class="momentum-fill" style="width:{pct:.0f}%"></div>
              </div>
              <div class="momentum-val">{score:.1f}</div>
            </div>"""
        bars_html += '</div>'
        st.markdown(bars_html, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="pixel-box">
          <div style="font-family:var(--font-silk);font-size:10px;color:var(--gb-mid);text-align:center;padding:20px 0;">
            MOMENTUM DATA PENDING — AWAITING SCANS
          </div>
        </div>
        """, unsafe_allow_html=True)

with col_right:
    if not tokens_df.empty and 'score' in tokens_df.columns:
        score_vals = tokens_df['score'].dropna()
        if len(score_vals):
            fig = go.Figure()
            fig.add_trace(go.Histogram(
                x=score_vals,
                nbinsx=10,
                marker_color='rgba(155,188,15,0.7)',
                marker_line_color='#306230',
                marker_line_width=1,
            ))
            fig.update_layout(
                paper_bgcolor='#0d1208',
                plot_bgcolor='#0a0e0a',
                font=dict(family='Silkscreen', color='#8bac0f', size=9),
                margin=dict(l=10, r=10, t=20, b=10),
                height=180,
                xaxis=dict(
                    gridcolor='rgba(48,98,48,0.3)',
                    title=dict(text='SCORE', font=dict(size=8)),
                    tickfont=dict(size=8),
                ),
                yaxis=dict(
                    gridcolor='rgba(48,98,48,0.3)',
                    title=dict(text='COUNT', font=dict(size=8)),
                    tickfont=dict(size=8),
                ),
                bargap=0.1,
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.markdown("""
        <div class="pixel-box" style="height:180px;display:flex;align-items:center;justify-content:center;">
          <div style="font-family:var(--font-silk);font-size:10px;color:var(--gb-mid);">NO CHART DATA</div>
        </div>
        """, unsafe_allow_html=True)

# ─── SECURITY ALERTS ──────────────────────────────────────────────────────────
st.markdown("""
<div class="section-header" style="margin-top:32px;">
  <div class="section-title">🚨 SECURITY ALERTS</div>
  <div class="section-line"></div>
</div>
""", unsafe_allow_html=True)

alerts_html = ""
if not tokens_df.empty and 'score' in tokens_df.columns:
    critical = tokens_df[tokens_df['score'] >= 8]
    high     = tokens_df[(tokens_df['score'] >= 7) & (tokens_df['score'] < 8)]
    timestamp_str = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

    if len(critical):
        syms = ", ".join(f"${s}" for s in critical['symbol'].head(3).tolist()) if 'symbol' in critical.columns else "N/A"
        alerts_html += f"""
        <div class="alert-box critical">
          <div class="alert-icon">⚠</div>
          <div class="alert-content">
            <div class="alert-title">CRITICAL THREAT DETECTED</div>
            <div>TOKENS: {syms}</div>
            <div>COUNT: {len(critical)} HIGH-RISK CANDIDATES</div>
            <div style="opacity:0.6;margin-top:4px;">{timestamp_str}</div>
          </div>
        </div>"""

    if len(high):
        syms = ", ".join(f"${s}" for s in high['symbol'].head(3).tolist()) if 'symbol' in high.columns else "N/A"
        alerts_html += f"""
        <div class="alert-box high">
          <div class="alert-icon">!</div>
          <div class="alert-content">
            <div class="alert-title">HIGH RISK TOKENS</div>
            <div>TOKENS: {syms}</div>
            <div>COUNT: {len(high)} FLAGGED FOR REVIEW</div>
            <div style="opacity:0.6;margin-top:4px;">{timestamp_str}</div>
          </div>
        </div>"""

    if not len(critical) and not len(high):
        alerts_html = """
        <div class="alert-box info">
          <div class="alert-icon">✓</div>
          <div class="alert-content">
            <div class="alert-title">SYSTEM NOMINAL</div>
            <div>NO HIGH-RISK TOKENS DETECTED IN CURRENT SCAN</div>
          </div>
        </div>"""
else:
    alerts_html = """
    <div class="alert-box info">
      <div class="alert-icon">○</div>
      <div class="alert-content">
        <div class="alert-title">MONITORING ACTIVE</div>
        <div>SCANNER INITIALIZED — AWAITING FIRST DATA STREAM</div>
      </div>
    </div>"""

st.markdown(alerts_html, unsafe_allow_html=True)

# ─── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="console-footer">
  <div class="footer-text">🔒 BLOCK BOY SECURITY CONSOLE V2.0  ∙  BUILT BY JOSEPH ALEXAN</div>
  <div class="footer-text">DATA: DEXSCREENER ∙ COINGECKO ∙ BIRDEYE  ∙  AUTO-SCAN: {auto_refresh}S</div>
  <div class="footer-text">⚡ POWERED BY SOLANA BLOCKCHAIN</div>
</div>
""", unsafe_allow_html=True)

# ─── AUTO-REFRESH ─────────────────────────────────────────────────────────────
time.sleep(auto_refresh)
st.rerun()