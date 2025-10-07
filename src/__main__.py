from pathlib import Path
import sys

from dotenv import load_dotenv

PACKAGE_DIR = Path(__file__).resolve().parent
SRC_ROOT = PACKAGE_DIR.parent
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

ENV_PATH = SRC_ROOT / ".env"

from loguru import logger

from trading_framework.logging_config import configure


def main() -> None:
    dotenv_loaded = load_dotenv(dotenv_path=ENV_PATH)
    configure()
    if not dotenv_loaded:
        logger.warning(f"No .env file found at {ENV_PATH}")

    logger.info("Demarrage du framework...")
    from datetime import datetime, timedelta, timezone
    from trading_framework.core.market_types import Timeframe as TF
    from trading_framework.data.alpaca_pipeline import fetch_alpaca_bars

    # Time window for the Alpaca request
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=2)

    # Fetch bars by using the core timeframe enum
    df = fetch_alpaca_bars(
        symbol="AAPL",
        timeframe=TF.MIN1,
        start=start,
        end=end,
        feed="iex",
    )

    print(df.head())
    print(len(df), "rows received")


if __name__ == "__main__":
    main()
