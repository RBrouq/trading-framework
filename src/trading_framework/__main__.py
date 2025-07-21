from loguru import logger

from trading_framework.logging_config import configure


def main() -> None:
    configure()
    logger.info("Démarrage du framework…")
    # …


if __name__ == "__main__":
    main()
