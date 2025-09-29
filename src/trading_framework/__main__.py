from loguru import logger

from trading_framework.logging_config import configure


def main() -> None:
    configure()
    logger.info("Démarrage du framework…")
    from datetime import datetime, timedelta, timezone
    from trading_framework.core.market_types import Timeframe as TF
    from trading_framework.data.alpaca_pipeline import fetch_alpaca_bars

    # Fenêtre temporelle
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=2)

    # Appel (tu passes TF du core, pas celui d'Alpaca)
    df = fetch_alpaca_bars(
        symbol="AAPL",
        timeframe=TF.MIN1,  # 👈 ton vocabulaire core
        start=start,
        end=end,
        feed="iex",  # ou "sip" si tu as l’abonnement
    )

    print(df.head())
    print(len(df), "lignes reçues")


if __name__ == "__main__":
    main()
