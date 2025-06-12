"""Logging utilities and configuration for PyPort."""

import logging

LOG_LEVEL_MAP = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


def init_logging(log_level: str) -> None:
    """Initialize logging configuration.

    Args:
        log_level: The logging level to set.
    """
    level = LOG_LEVEL_MAP[log_level]
    logging.basicConfig(level=level,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                            logging.FileHandler("app.log"),
                            logging.StreamHandler()
                        ])
