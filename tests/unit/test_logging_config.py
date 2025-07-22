import logging

import pytest

from trading_framework.logging_config import configure


@pytest.fixture(autouse=True)
def reset_logging():
    """
    Remove all handlers from root logger before and after each test.
    """
    root = logging.getLogger()
    existing = list(root.handlers)
    for h in existing:
        root.removeHandler(h)
    yield
    for h in list(root.handlers):
        root.removeHandler(h)


def test_configure_creates_log_dir_and_writes_log(tmp_path):
    log_dir = tmp_path / "logs"
    # Configure logging
    configure(level=logging.INFO, log_dir=log_dir)
    # Log a test message
    logger = logging.getLogger("test_logger")
    logger.info("test message")
    # Ensure log file exists
    log_file = log_dir / "framework.log"
    assert log_file.exists(), "Log file should be created"
    # Read log content
    content = log_file.read_text(encoding="utf-8")
    assert "test message" in content, (
        "Logged message should appear in the file"
    )


def test_configure_idempotent_not_dup_handlers(tmp_path):
    log_dir = tmp_path / "logs2"
    # First configuration
    configure(level=logging.DEBUG, log_dir=log_dir)
    handlers_first = list(logging.getLogger().handlers)
    # Second configuration with same parameters
    configure(level=logging.DEBUG, log_dir=log_dir)
    handlers_second = list(logging.getLogger().handlers)
    # Handlers should not be duplicated
    assert handlers_first == handlers_second, (
        "Handlers should remain the same after reconfigure"
    )


def test_custom_log_file_name(tmp_path):
    log_dir = tmp_path / "mylogs"
    configure(
        level=logging.WARNING, log_dir=log_dir, log_file_name="custom.log"
    )
    logger = logging.getLogger("custom_logger")
    logger.warning("warn message")
    custom_file = log_dir / "custom.log"
    assert custom_file.exists(), "Custom log file should be created"
    assert "warn message" in custom_file.read_text(encoding="utf-8")
