# logging_config.py
# -*- coding: utf-8 -*-
"""
Configuration centralisée du logging pour le Trading Framework.
Crée un dossier de logs utilisateur, configure un RotatingFileHandler,
et propose une intégration transparente avec loguru si installé.
"""
from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path
from types import FrameType
from typing import Optional, Union

# Vérifie la disponibilité de loguru pour interconnexion
try:
    from loguru import logger as _loguru_logger  # type: ignore[import]

    _HAS_LOGURU: bool = True
except ImportError:
    _HAS_LOGURU = False


class InterceptHandler(logging.Handler):
    """
    Redirige les logs du module `logging` vers loguru si disponible.
    """

    def emit(self, record: logging.LogRecord) -> None:
        if _HAS_LOGURU:
            level: int = record.levelno
            frame: Optional[FrameType] = logging.currentframe()
            depth: int = 2
            # Recherche l'appelant hors logging internals
            while frame is not None and frame.f_code.co_filename:
                frame = frame.f_back
                depth += 1
            _loguru_logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )
        else:
            super().emit(record)


def configure(
    level: Optional[int] = None,
    log_dir: Optional[Union[Path, str]] = None,
    log_file_name: str = "framework.log",
    max_bytes: int = 5_000_000,
    backup_count: int = 5,
    use_loguru: bool = False,
) -> None:
    """
    Initialise et configure le logging centralisé.

    Args:
        level: Niveau de log (logging.DEBUG, INFO...).
            Si None => lit la variable d'env TF_LOG_LEVEL ou INFO.
        log_dir: Dossier de stockage des logs.
            Si None => ~/.trading_framework/logs.
        log_file_name: Nom du fichier tournant.
        max_bytes: Taille max d'un fichier avant rotation.
        backup_count: Nombre de backups.
        use_loguru: Active loguru en interceptant stdlib.
    """
    # Niveau par défaut
    if level is None:
        env_level: str = os.getenv("TF_LOG_LEVEL", "INFO").upper()
        level = getattr(logging, env_level, logging.INFO)

    # Détermine et crée le dossier
    log_path: Path
    if log_dir is None:
        log_path = Path.home() / ".trading_framework" / "logs"
    else:
        log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    # Rotating handler
    rotating: RotatingFileHandler = RotatingFileHandler(
        filename=log_path / log_file_name,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding="utf-8",
    )
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s")
    rotating.setFormatter(fmt)

    # Configure logger racine
    root = logging.getLogger()
    root.setLevel(level)

    if use_loguru and _HAS_LOGURU:
        # Intercepte les handlers stdlib
        interceptor = InterceptHandler()
        interceptor.setLevel(level)
        # Remplace les RotatingFileHandler existants
        root.handlers = [
            h for h in root.handlers if not isinstance(h, RotatingFileHandler)
        ]
        root.addHandler(interceptor)
        # Configure loguru séparément
        _loguru_logger.remove()
        _loguru_logger.add(
            log_path / f"{log_file_name}.loguru",
            rotation=max_bytes,
            retention=backup_count,
            level=level,
            format="{time} | {level} | {name} | {message}",
            serialize=False,
        )
    else:
        # Ajoute le handler RotatingFileHandler s'il n'existe pas
        if not any(isinstance(h, RotatingFileHandler) for h in root.handlers):
            root.addHandler(rotating)
