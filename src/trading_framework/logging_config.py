"""
logging_config.py

Configuration centralisée du logging pour le Trading Framework.
Crée un dossier de logs utilisateur, configure un RotatingFileHandler,
et propose une intégration transparente avec loguru si installé.
"""

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Tentative d'intégration à loguru
try:
    from loguru import logger as _loguru_logger

    _HAS_LOGURU = True
except ImportError:
    _HAS_LOGURU = False


class InterceptHandler(logging.Handler):
    """
    Handler pour rediriger les logs stdlib vers loguru.
    """

    def emit(self, record: logging.LogRecord) -> None:
        if _HAS_LOGURU:
            # Récupère le niveau loguru correspondant
            level = record.levelno
            frame = logging.currentframe()
            depth = 2
            # Monte dans la pile pour localiser l'appelant
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            _loguru_logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )
        else:
            super().emit(record)


def configure(
    level: int = None,
    log_dir: Path | str = None,
    log_file_name: str = "framework.log",
    max_bytes: int = 5_000_000,
    backup_count: int = 5,
    use_loguru: bool = False,
) -> None:
    """
    Initialise et configure le logging centralisé.

    Args:
        level: Niveau de log (logging.DEBUG, INFO...). Si None, lit
        TF_LOG_LEVEL ou INFO.
        log_dir: Dossier de stockage des fichiers de log. Si None, utilise
          ~/.trading_framework/logs.
        log_file_name: Nom du fichier de log tournant.
        max_bytes: Taille max d'un fichier avant rotation.
        backup_count: Nombre de fichiers de backup conservés.
        use_loguru: Active la redirection des logs standard vers loguru si
        installé.
    """
    # Niveau par défaut via variable d'environnement
    if level is None:
        lvl_name = os.getenv("TF_LOG_LEVEL", "INFO").upper()
        level = getattr(logging, lvl_name, logging.INFO)

    # Chemin du dossier de logs
    if log_dir is None:
        log_dir = Path.home() / ".trading_framework" / "logs"
    else:
        log_dir = Path(log_dir)
    log_dir.mkdir(parents=True, exist_ok=True)

    # Handler tournant
    handler = RotatingFileHandler(
        filename=log_dir / log_file_name,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)

    # Logger racine
    root = logging.getLogger()
    root.setLevel(level)

    # Nettoie les handlers existants de même type
    if use_loguru and _HAS_LOGURU:
        # Intercepter les logs stdlib vers loguru
        intercept = InterceptHandler()
        intercept.setLevel(level)
        root.handlers = [
            h for h in root.handlers if not isinstance(h, RotatingFileHandler)
        ]
        root.addHandler(intercept)
    else:
        # Empêche duplication de handlers RotatingFileHandler
        if not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
            root.addHandler(handler)

    # Si loguru est présent et souhaité, configure son handler
    if use_loguru and _HAS_LOGURU:
        # Optionnel: supprime handlers par défaut de loguru
        _loguru_logger.remove()
        _loguru_logger.add(
            log_dir / f"{log_file_name}.loguru",
            rotation=max_bytes,
            retention=backup_count,
            level=level,
            format="{time} | {level} | {name} | {message}",
            serialize=False,
        )
