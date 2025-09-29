from __future__ import annotations

from typing import Protocol, runtime_checkable

import pandas as pd

from .market_types import Source, Symbol, Timeframe

# ---- Minimal schema all normalized bar DataFrames must satisfy ----
BAR_COLUMNS = (
    "ts",  # timezone-aware pandas.Timestamp (UTC)
    "open",
    "high",
    "low",
    "close",
    "volume",
    "symbol",  # str (ticker)
    "timeframe",  # str (Timeframe.value)
    "source",  # str or None (data provider)
)


def validate_bars_df(df: pd.DataFrame) -> None:
    """
    Validate that a DataFrame satisfies the minimal bar schema.
    - All required columns exist.
    - 'ts' column is tz-aware (UTC recommended).
    - 'volume' is non-negative.
    Raises ValueError if any check fails.
    """
    missing = [c for c in BAR_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")

    if df["ts"].dt.tz is None:
        raise ValueError("'ts' must be timezone-aware (UTC recommended)")

    if (df["volume"] < 0).any():
        raise ValueError("Negative volume detected")


@runtime_checkable
class BarReader(Protocol):
    """
    Read normalized OHLCV bars.

    Implementations (CSV, Parquet, Alpaca, IBKR, etc.) must return a DataFrame
    containing at least BAR_COLUMNS and already normalized to UTC.
    """

    def load(
        self,
        symbol: Symbol,
        timeframe: Timeframe,
        source: Source | None = None,
        start: pd.Timestamp | None = None,
        end: pd.Timestamp | None = None,
    ) -> pd.DataFrame: ...

    # The ellipsis `...` means "no implementation here" (interface only).


@runtime_checkable
class BarWriter(Protocol):
    """
    Persist normalized OHLCV bars.

    Implementations (Parquet/SQL/S3/…) should be idempotent (no duplicates)
    and accept a DataFrame that satisfies BAR_COLUMNS.
    """

    def write(self, df: pd.DataFrame) -> None: ...

    # Returns None to signal "procedure" semantics: write-or-raise, no value.
