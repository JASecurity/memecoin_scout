import asyncio
import os
import pandas as pd
from app.data_sources.dexscreener import fetch_new_listings
from app.filters import filter_tokens
from app.scorer import score_tokens
from app.alerting.telegram_alert import send_telegram_alert
from app.schemas import FiltersConfig
from app.logger import log_token
from app.momentum_tracker import log_momentum, detect_momentum_spike


async def process_token(token, cfg):
    """
    Process each token: filter, score, momentum check, log, and alert.
    """
    try:
        score = score_tokens(token)
        log_momentum(token)
        if detect_momentum_spike(token):
            msg = (
                f"[MOMENTUM SPIKE]\n"
                f"Symbol: {token.symbol}\n"
                f"Chain: {token.chain}\n"
                f"Liquidity: ${token.liquidity_usd:,.0f}\n"
                f"Volume 1h: ${token.volume_usd_1h:,.0f}\n"
            )
            await send_telegram_alert(msg)

        if filter_tokens(token, cfg):
            log_token(token)
            alert = (
                f"🚀 NEW TOKEN FOUND 🚀\n"
                f"Symbol: {token.symbol}\n"
                f"Chain: {token.chain}\n"
                f"Liquidity: ${token.liquidity_usd:,.0f}\n"
                f"Volume 1h: ${token.volume_usd_1h:,.0f}\n"
                f"Holders: {token.holders}\n"
                f"LP Lock: {token.lp_lock_ratio * 100:.1f}%"
            )
            await send_telegram_alert(alert)

    except Exception as e:
        print(f"[error] while processing token {getattr(token, 'symbol', '?')}: {e}")


async def main():
    """
    Main bot loop — fetches, filters, scores, and alerts new tokens.
    """
    print("[live] Memecoin Scout + Momentum started…")
    cfg = FiltersConfig(
        chains=["solana"],
        min_liquidity_usd=3000,
        max_fdv_usd=10000000,
        min_holders=5,
        min_age_minutes=5,
        max_buy_tax_bps=400,
        max_sell_tax_bps=400,
        require_owner_renounced_or_timelock=False,
        require_mint_authority_revoked=False,
        min_lp_lock_ratio=0.5,
    )

    while True:
        try:
            print("[info] Fetching new tokens from DexScreener…")
            tokens = await fetch_new_listings(cfg.chains)
            print(f"[debug] {len(tokens)} tokens fetched. Filtering and scoring…")

            if not tokens:
                print("[-] No tokens fetched.")
            else:
                for token in tokens:
                    await process_token(token, cfg)

        except Exception as e:
            print(f"[error] main loop: {e}")

        print("[sleep] Waiting 3.0 minutes before next scan…")
        await asyncio.sleep(180)  # 3 minutes


if __name__ == "__main__":
    asyncio.run(main())
