__version__ = "0.1.0"


def init_logging(level: int = 20) -> None:  # logging.INFO
    from .logging_config import configure

    configure(level)
