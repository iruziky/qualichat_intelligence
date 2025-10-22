# -*- coding: utf--8 -*-
"""Application-wide logging setup."""
import sys

from loguru import logger

# Configure logger
config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>",
        },
    ],
    "extra": {"user": "someone"},
}

logger.configure(**config)

