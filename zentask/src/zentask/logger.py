"""Logging configuration for Zentask."""

import logging
import sys

def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Set up application logging."""
    logger = logging.getLogger("zentask")
    logger.setLevel(level)

    # Remove existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    return logger

# Global logger instance
logger = setup_logging()