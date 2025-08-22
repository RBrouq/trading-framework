from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import NewType

import pandas as pd

"""
Core types for the trading framework (thin core).
- Aliases: Symbol, Source
- Enums: Timeframe, AssetClass (optional but handy)
- Dataclass: Bar (OHLCV), with light invariants checker

Notes
-----
* All timestamps (`ts`) MUST be timezone-aware in UTC.
* Prices/volume stored as float for simplicity; can be swapped later to Decimal
/ints.
* This module contains no I/O or business logic.
"""

# ----------------------------- Type aliases ------------------------------ #
Symbol = NewType("Symbol", str)
Source = NewType("Source", str)


# ------------------------------- Enums ----------------------------------- #
class AssetClass(Enum):
    """High-level asset taxonomy (extend as needed)."""

    EQUITY = "equity"
    FUTURES = "futures"
    FX = "fx"
    OPTION = "option"
    ETF = "etf"
    OTHER = "other"


class Timeframe(Enum):
    """Standardized bar granularities used across the framework."""

    TICK = "tick"
    MIN1 = "1Min"
    MIN5 = "5Min"
    MIN15 = "15Min"
    MIN30 = "30Min"
    H1 = "1H"
    H4 = "4H"
    D1 = "1D"
    W1 = "1W"
    M1 = "1M"

    @classmethod
    def from_str(cls, s: str) -> Timeframe:
        """Parse common aliases and return a normalized Timeframe value.

        Examples
        --------
        >>> Timeframe.from_str("1min") is Timeframe.MIN1
        True
        >>> Timeframe.from_str("1H") is Timeframe.H1
        True
        >>> Timeframe.from_str("1d") is Timeframe.D1
        True
        """
        key = s.strip().lower()
        # direct match on enum values
        for tf in cls:
            if key == tf.value.lower():
                return tf
        aliases = {
            "tick": "tick",
            "1m": "1Min",
            "1min": "1Min",
            "5m": "5Min",
            "5min": "5Min",
            "15m": "15Min",
            "15min": "15Min",
            "30m": "30Min",
            "30min": "30Min",
            "1h": "1H",
            "4h": "4H",
            "1d": "1D",
            "1w": "1W",
            "1mo": "1M",
            "1mth": "1M",
        }
        try:
            return cls(aliases[key])
        except KeyError as e:
            raise ValueError(f"Unknown timeframe alias: {s!r}") from e


# ------------------------------- Bar ------------------------------------- #
@dataclass(frozen=True, slots=True)
class Bar:
    """Normalized OHLCV bar.

    Invariants
    ----------
    * `ts` MUST be a timezone-aware pandas.Timestamp (UTC recommended).
    * `low <= open, close <= high` must hold.
    * `volume >= 0`.
    """

    symbol: Symbol
    ts: pd.Timestamp
    open: float
    high: float
    low: float
    close: float
    volume: float
    timeframe: Timeframe
    source: Source | None

    def check_invariants(self) -> None:
        """Raise ValueError if basic OHLCV invariants are violated."""
        if self.ts.tzinfo is None:
            raise ValueError(
                "Bar.ts must be a timezone-aware (UTC recommended)"
            )
        if not (
            self.low <= self.open <= self.high
            and self.low <= self.close <= self.high
        ):
            raise ValueError(
                "OHLC invariants violated: expected low <= open, close <= high"
            )
        if self.volume < 0:
            raise ValueError("volume must be >= 0")
