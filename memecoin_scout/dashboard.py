# dashboard.py
# Live dashboard for Memecoin Scout (reads token_logs.csv and momentum.csv)

import os
from pathlib import Path
from datetime import datetime, timezone

import pandas as pd
import streamlit as st
import plotly.express as px

# ---------------------------
# Paths
# ---------------------------
ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT.parent / "token_logs.csv"
MOMENTUM_FILE = ROOT / "app" / "data" / "momentum.csv"

# ---------------------------
# Helpers
# ---------------------------
def _coerce_num(series):
    if series is None:
        return series
    return pd.to_numeric(series.astype(str).str.replace(",", "", regex=False).str.replace("$", "", regex=False), errors="coerce")

@st.cache_data(ttl=5.0, show_spinner=False)
def load_logs():
    if LOG_FILE.exists():
        df = pd.read_csv(LOG_FILE)
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", utc=True)
        for col in ["score", "holders", "momentum_5m", "momentum_15m"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        if "liquidity" in df.columns:
            df["liquidity_num"] = _coerce_num(df["liquidity"])
        if "volume" in df.columns:
            df["volume_num"] = _coerce_num(df["volume"])
        if "lp_lock" in df.columns:
            df["lp_lock_num"] = pd.to_numeric(df["lp_lock"], errors="coerce")
        df = df.sort_values("timestamp", ascending=False)
        return df
    cols = ["timestamp","symbol","chain","score","liquidity","volume","holders","lp_lock","momentum_5m","momentum_15m","link"]
    return pd.DataFrame(columns=cols)

@st.cache_data(ttl=5.0, show_spinner=False)
def load_momentum():
    if MOMENTUM_FILE.exists():
        df = pd.read_csv(MOMENTUM_FILE)
        if "ts" in df.columns:
            df["ts"] = pd.to_datetime(df["ts"], unit="s", utc=True, errors="coerce")
        for col in ["price_usd", "liquidity_usd"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
        return df
    return pd.DataFrame(columns=["ts","address","symbol","price_usd","liquidity_usd"])

def fmt_dt(dt):
    if pd.isna(dt) or dt is None:
        return "-"
    return dt.tz_convert("America/Toronto").strftime("%Y-%m-%d %H:%M:%S")

def color_score(val):
    if pd.isna(val):
        return ""
    val = float(val)
    if val >= 85:
        return "High"
    elif val >= 70:
        return "Medium"
    else:
        return "Low"

# ---------------------------
# UI Setup
# ---------------------------
st.set_page_config(
    page_title="Memecoin Scout Dashboard",
    page_icon="💰",
    layout="wide",
)

st.title("Memecoin Scout — Live Dashboard")

# Sidebar
st.sidebar.header("Filters and Controls")
refresh_secs = st.sidebar.slider("Auto-refresh (seconds)", min_value=5, max_value=120, value=20, step=5)
min_score = st.sidebar.slider("Minimum Score", 0, 100, 80)
require_momentum = st.sidebar.checkbox("Require Momentum > +20%", value=False)
today_only = st.sidebar.checkbox("Show only today's alerts", value=False)
symbol_filter = st.sidebar.text_input("Search symbol", value="")
chain_sel = st.sidebar.multiselect("Chains", options=["solana", "ethereum", "bsc"], default=["solana"])

st.caption(f"Data files: {LOG_FILE} and {MOMENTUM_FILE}")

# ---------------------------
# Load Data
# ---------------------------
logs = load_logs()
mom = load_momentum()

if not logs.empty:
    df = logs.copy()
    if chain_sel:
        df = df[df["chain"].isin(chain_sel)]
    if symbol_filter:
        df = df[df["symbol"].astype(str).str.contains(symbol_filter, case=False, na=False)]
    if min_score:
        df = df[df["score"] >= min_score]
    if require_momentum:
        df = df[(df["momentum_5m"] >= 20) | (df["momentum_15m"] >= 20)]
    if today_only:
        df = df[df["timestamp"].dt.date == datetime.now(timezone.utc).date()]
else:
    df = logs

# ---------------------------
# KPI Metrics
# ---------------------------
col1, col2, col3, col4 = st.columns(4)
if df.empty:
    col1.metric("Total Alerts", 0)
    col2.metric("Unique Tokens", 0)
    col3.metric("Last Scan", "-")
    col4.metric("Avg Score", "-")
else:
    col1.metric("Total Alerts", len(df))
    col2.metric("Unique Tokens", df["symbol"].nunique())
    col3.metric("Last Scan", fmt_dt(df["timestamp"].max()))
    col4.metric("Avg Score", f"{df['score'].mean():.1f}")

st.markdown("---")

# ---------------------------
# Token Table
# ---------------------------
st.subheader("Top Tokens (Filtered View)")

if df.empty:
    st.info("No tokens match the filters right now.")
else:
    df["Score Level"] = df["score"].apply(color_score)
    df["DexScreener"] = df["symbol"].apply(lambda s: f"[Open](https://dexscreener.com/solana/{s})")
    df["Birdeye"] = df["symbol"].apply(lambda s: f"[Chart](https://birdeye.so/token/{s}?chain=solana)")
    show_cols = ["timestamp","symbol","Score Level","score","liquidity","volume","holders","lp_lock","momentum_5m","momentum_15m","DexScreener","Birdeye"]
    st.dataframe(df[show_cols], use_container_width=True, height=400)

# ---------------------------
# Momentum Chart
# ---------------------------
st.markdown("---")
st.subheader("Momentum Charts")

if mom.empty:
    st.caption("Momentum data will appear once your bot logs snapshots.")
else:
    symbol_choice = st.selectbox("Select Token", sorted(mom["symbol"].dropna().unique()))
    sub_df = mom[mom["symbol"] == symbol_choice].sort_values("ts")

    col1, col2 = st.columns(2)
    with col1:
        fig_price = px.line(sub_df, x="ts", y="price_usd", title=f"{symbol_choice} — Price (USD)")
        st.plotly_chart(fig_price, use_container_width=True)
    with col2:
        fig_liq = px.line(sub_df, x="ts", y="liquidity_usd", title=f"{symbol_choice} — Liquidity (USD)")
        st.plotly_chart(fig_liq, use_container_width=True)

# ---------------------------
# Log Viewer
# ---------------------------
st.markdown("---")
st.subheader("Recent Alerts Log")

if logs.empty:
    st.caption("No alerts yet. Keep your bot running.")
else:
    st.dataframe(
        logs.head(100)[["timestamp","symbol","chain","score","momentum_5m","momentum_15m","link"]],
        use_container_width=True,
        height=300
    )

st.caption("Dashboard auto-refreshes every few seconds. Keep your bot running for live updates.")
