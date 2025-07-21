from trading_framework.logging_config import configure_logging
from loguru import logger


def main():
    configure_logging()
    logger.info("Démarrage du framework…")
    # …
