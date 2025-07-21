# tests/unit/test_logging_config.py
from loguru import logger

from trading_framework.logging_config import configure


def test_configure_logging(tmp_path, capsys) -> None:
    log_file = tmp_path / "app.log"
    configure(str(log_file))
    logger.debug("debug-msg")
    logger.info("info-msg")
    # on vérifie que le fichier a été créé et contient "debug-msg"
    content = log_file.read_text()
    assert "debug-msg" in content
    assert "info-msg" in content
