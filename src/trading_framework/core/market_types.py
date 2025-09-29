from __future__ import annotations
from enum import Enum
from typing import NewType

# Aliases (contrat de domaine)
Symbol = NewType("Symbol", str)
Source = NewType("Source", str)


class AssetClass(Enum):
    EQUITY = "equity"
    FUTURES = "futures"
    FX = "fx"
    OPTION = "option"
    ETF = "etf"
    OTHER = "other"


class Timeframe(Enum):
    # Ticks & minutes
    TICK = "tick"
    MIN1 = "1Min"
    MIN2 = "2Min"
    MIN5 = "5Min"
    MIN10 = "10Min"
    MIN15 = "15Min"
    MIN30 = "30Min"
    # Hours
    H1 = "1H"
    H2 = "2H"
    H4 = "4H"
    H6 = "6H"
    H8 = "8H"
    H12 = "12H"
    # Days / Weeks / Months / Years
    D1 = "1D"
    W1 = "1W"
    M1 = "1M"  # 1 month
    Q1 = "1Q"  # 1 quarter
    Y1 = "1Y"  # 1 year

    @classmethod
    def from_str(cls, s: str) -> Timeframe:
        """Accepte aliases usuels: 1m, 5min, 1h, 1d, 1w, 1mo|1mth, 1q, 1y, etc."""
        key = s.strip().lower()

        # valeur exacte (ex: "1min", "1h", "1d"...)
        for tf in cls:
            if key == tf.value.lower():
                return tf

        aliases = {
            "tick": "tick",
            "1m": "1Min",
            "1min": "1Min",
            "2m": "2Min",
            "2min": "2Min",
            "5m": "5Min",
            "5min": "5Min",
            "10m": "10Min",
            "10min": "10Min",
            "15m": "15Min",
            "15min": "15Min",
            "30m": "30Min",
            "30min": "30Min",
            "1h": "1H",
            "2h": "2H",
            "4h": "4H",
            "6h": "6H",
            "8h": "8H",
            "12h": "12H",
            "1d": "1D",
            "1w": "1W",
            "1mo": "1M",
            "1mth": "1M",
            "1month": "1M",
            "1q": "1Q",
            "1quarter": "1Q",
            "1y": "1Y",
            "1yr": "1Y",
            "1year": "1Y",
        }
        try:
            return cls(aliases[key])
        except KeyError as e:
            raise ValueError(f"Unknown timeframe alias: {s!r}") from e

    def as_str(self) -> str:
        """Chaîne canonique pour stockage DataFrame/Parquet."""
        return self.value


# Schéma minimal recommandé pour stockage
BAR_COLUMNS = (
    "ts",
    "symbol",
    "timeframe",
    "open",
    "high",
    "low",
    "close",
    "volume",
)
# Colonnes optionnelles courantes (si dispo)
BAR_OPTIONAL = ("vwap", "trade_count", "source")
