import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure(level: int = logging.INFO) -> None:
    # Crée le dossier ~/.trading_framework/logs s'il n'existe pas
    log_dir = Path.home() / ".trading_framework" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Fichier tournant : 5 MB max, 5 backups
    handler = RotatingFileHandler(
        filename=log_dir / "framework.log",
        maxBytes=5_000_000,
        backupCount=5,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(level)
    # Évite les doublons si configure() est appelé plusieurs fois
    if not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
        root.addHandler(handler)
