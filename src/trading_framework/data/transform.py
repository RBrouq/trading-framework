from __future__ import annotations
import pandas as pd
from typing import Iterable
from trading_framework.core.market_types import (
    BAR_COLUMNS,
    BAR_OPTIONAL,
    Timeframe,
)


def _ensure_utc_series(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, utc=True)


def normalize_bars_df(
    df_raw: pd.DataFrame,
    *,
    symbol: str | None = None,  # si None, lu depuis df_raw["symbol"]
    timeframe: str | Timeframe = "1Min",
    source: str | None = None,  # ex: "alpaca" (optionnel)
    extra_keep: Iterable[str] = ("vwap", "trade_count"),
    place_timeframe_after_symbol: bool = True,  # juste pour l'ordre visuel
) -> pd.DataFrame:
    """
    Transforme un DataFrame brut en schéma standard minimal:
    ts (UTC), symbol, timeframe, open, high, low, close, volume
    + conserve vwap/trade_count si présents (ou les crée en NA)
    """

    if df_raw.empty:
        # DF vide mais colonnes attendues
        cols = list(BAR_COLUMNS) + [c for c in extra_keep if c in BAR_OPTIONAL]
        if source is not None:
            cols += ["source"]
        return pd.DataFrame(columns=cols)

    df = df_raw.copy()

    # 1) ts (UTC) depuis 'timestamp' si présent, sinon exige 'ts'
    if "timestamp" in df.columns and "ts" not in df.columns:
        df["ts"] = _ensure_utc_series(df["timestamp"])
        df.drop(columns=["timestamp"], inplace=True)
    elif "ts" in df.columns:
        df["ts"] = _ensure_utc_series(df["ts"])
    else:
        raise ValueError("Aucune colonne 'timestamp' ou 'ts' trouvée")

    # 2) symbol
    if symbol is not None:
        df["symbol"] = symbol
    if "symbol" not in df.columns:
        raise ValueError("Pas de colonne 'symbol' et aucun symbole fourni.")
    df["symbol"] = df["symbol"].astype(str).str.upper()

    # 3) timeframe -> chaîne canonique
    tf_enum = (
        timeframe
        if isinstance(timeframe, Timeframe)
        else Timeframe.from_str(str(timeframe))
    )
    df["timeframe"] = tf_enum.as_str()

    # 4) cast numérique de base (si colonnes présentes)
    for col in ("open", "high", "low", "close", "volume"):
        if col not in df.columns:
            raise ValueError(f"Colonne manquante: {col}")
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 5) colonnes optionnelles (vwap, trade_count)
    for col in extra_keep:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        else:
            df[col] = pd.NA

    # 6) source (optionnelle)
    if source is not None:
        df["source"] = str(source)

    # 7) ordre de colonnes
    if place_timeframe_after_symbol:
        ordered = [
            "ts",
            "symbol",
            "timeframe",
            "open",
            "high",
            "low",
            "close",
            "volume",
        ]
    else:
        ordered = [
            "ts",
            "symbol",
            "open",
            "high",
            "low",
            "close",
            "volume",
            "timeframe",
        ]

    for col in extra_keep:
        if col in df.columns:
            ordered.append(col)
    if source is not None:
        ordered.append("source")

    df = df[ordered].sort_values(["symbol", "ts"]).reset_index(drop=True)
    return df
