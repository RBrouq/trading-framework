# tests/unit/test_logging_config.py
from loguru import logger

from trading_framework.logging_config import configure_logging


def test_configure_logging(tmp_path, capsys) -> None:
    log_file = tmp_path / "app.log"
    configure_logging(str(log_file))
    logger.debug("debug-msg")
    logger.info("info-msg")
    # on vérifie que le fichier a été créé et contient "debug-msg"
    content = log_file.read_text()
    assert "debug-msg" in content
    assert "info-msg" in content
