# trading_framework/data/alpaca_pipeline.py
import os
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, find_dotenv
import pandas as pd
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame  # enum Alpaca

from trading_framework.core.market_types import (
    Timeframe as TF,
)  # ton enum core
from trading_framework.data.transform import normalize_bars_df

# --- mapping core -> alpaca ---
_ALPACA_FROM_CORE = {
    TF.MIN1: TimeFrame.Minute,
    TF.H1: TimeFrame.Hour,
    TF.D1: TimeFrame.Day,
    # ajoute d'autres si tu veux gérer plus de granularités côté Alpaca
}


def _to_alpaca_tf(tf: TF) -> TimeFrame:
    try:
        return _ALPACA_FROM_CORE[tf]
    except KeyError:
        raise ValueError(f"Timeframe non supporté par Alpaca: {tf}")


def fetch_alpaca_bars(
    symbol: str,
    timeframe: TF = TF.MIN1,  # 👈 vocabulaire du core en paramètre
    start: datetime | None = None,
    end: datetime | None = None,
    feed: str = "iex",
) -> pd.DataFrame:
    """Fetch (Alpaca) -> normalize (core). L'appelant ne voit que TF (core)."""
    load_dotenv(find_dotenv())
    api = os.getenv("ALPACA_API_KEY")
    secret = os.getenv("ALPACA_SECRET_KEY")
    if not api or not secret:
        raise RuntimeError("SALUT FRERO ALPACA_* ou APCA_*")

    end = end or datetime.now(timezone.utc)
    start = start or (end - timedelta(days=5))

    client = StockHistoricalDataClient(api, secret)
    bars = client.get_stock_bars(
        StockBarsRequest(
            symbol_or_symbols=symbol,
            timeframe=_to_alpaca_tf(timeframe),  # 👈 conversion interne
            start=start,
            end=end,
            feed=feed,
        )
    )
    df_raw = bars.df.reset_index()

    # Normalisation avec le TF du core (aucune ambiguïté)
    df = normalize_bars_df(
        df_raw,
        symbol=symbol,
        timeframe=timeframe,  # 👈 on reste en TF (core)
        source="alpaca",
        place_timeframe_after_symbol=True,
    )
    return df
