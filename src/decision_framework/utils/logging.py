"""
Logging Utilities

This module provides logging functionality for the decision framework.
"""

import logging
from typing import Optional
from pathlib import Path

def setup_logger(
    name: str,
    level: int = logging.INFO,
    log_file: Optional[Path] = None
) -> logging.Logger:
    """Set up a logger with the specified configuration."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
