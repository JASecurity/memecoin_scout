import time
import httpx
from typing import List
from ..schemas import TokenInfo, LiquidityInfo, VolumeInfo, HolderStats

DEX_URLS = [
    # current known working endpoints
    "https://api.dexscreener.com/latest/dex/tokens/solana",
    "https://api.dexscreener.com/latest/dex/pairs/solana",
    "https://api.dexscreener.com/latest/dex/search?q=solana"
]

async def fetch_new_listings(max_age_minutes: int = 60) -> List[TokenInfo]:
    """
    Try multiple DexScreener endpoints until one works.
    Normalize into TokenInfo objects.
    """
    data = None
    last_error = None

    for url in DEX_URLS:
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                r = await client.get(url)
                r.raise_for_status()
                data = r.json()
                print(f"[debug] DexScreener endpoint OK: {url}")
                break
        except Exception as e:
            last_error = e
            print(f"[warn] DexScreener endpoint failed: {url} ({e})")

    if not data:
        raise last_error or RuntimeError("All DexScreener endpoints failed")

    pairs = data.get("pairs") or data.get("tokens") or []
    now_ms = int(time.time() * 1000)
    tokens: List[TokenInfo] = []

    for p in pairs:
        created_ms = p.get("pairCreatedAt") or now_ms
        age_m = max(0, int((now_ms - int(created_ms)) / 1000 / 60))

        liq_usd = 0.0
        if isinstance(p.get("liquidity"), dict):
            liq_usd = float(p["liquidity"].get("usd") or 0)

        vol = p.get("volume") or {}
        vol_1h = float(vol.get("h1") or 0)
        vol_24h = float(vol.get("h24") or 0)
        price_usd = float(p.get("priceUsd") or 0)

        txns = p.get("txns") or {}
        h5 = txns.get("h5") or {}
        trades_5m = int(h5.get("buys") or 0) + int(h5.get("sells") or 0)

        base = p.get("baseToken") or {}
        symbol = base.get("symbol") or p.get("info", {}).get("baseSymbol") or "UNKNOWN"
        address = base.get("address") or p.get("pairAddress") or ""

        token = TokenInfo(
            symbol=symbol,
            chain="solana",
            address=address,
            price_usd=price_usd,
            liquidity=LiquidityInfo(usd=liq_usd, lp_lock_ratio=0.0),
            volume=VolumeInfo(usd_1h=vol_1h, usd_24h=vol_24h),
            holders=HolderStats(holder_count=0, top1_pct=0.0, top5_pct=0.0),
            age_minutes=age_m,
            fdv_usd=float(p.get("fdv") or 0),
            dex_trades_5m=trades_5m,
        )

        if age_m <= max_age_minutes:
            tokens.append(token)

    print(f"[debug] number of pairs: {len(tokens)}")
    return tokens
