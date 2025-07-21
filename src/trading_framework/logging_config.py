import sys

from loguru import logger


def configure_logging(log_file: str = "logs/trading.log"):
    # supprime le handler par défaut
    logger.remove()
    # console : INFO et plus
    logger.add(sys.stderr, level="INFO", backtrace=True, diagnose=True)
    # fichier : rotation tous les jours, rétention 7 jours
    logger.add(
        log_file,
        rotation="1 day",
        retention="7 days",
        level="DEBUG",
        format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}",
    )
