from loguru import logger

from trading_framework.logging_config import configure_logging


def main() -> None:
    configure_logging()
    logger.info("Démarrage du framework…")
    # …
