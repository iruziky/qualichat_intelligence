# -*- coding: utf-8 -*-
"""
Applies necessary patches to third-party libraries at runtime.
This module should be imported at the very beginning of the application's entry point.
"""

import sys
from app.core.logger import logger


def apply_patches():
    """
    Applies all registered patches.
    """
    _patch_sqlite3()


def _patch_sqlite3():
    """
    Replaces the system's default sqlite3 with a newer version (pysqlite3-binary).
    This is required for ChromaDB compatibility on systems with older sqlite3 versions.
    """
    try:
        __import__("pysqlite3")
        sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")
        logger.debug("Successfully patched sqlite3 with pysqlite3-binary.")
    except ImportError:
        logger.warning(
            "pysqlite3-binary not found. "
            "ChromaDB might fail if the system's sqlite3 is too old."
        )

