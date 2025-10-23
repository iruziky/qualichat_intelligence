# -*- coding: utf-8 -*-
"""Repository for persisting chat history using SQLite."""
import sqlite3
import json
from pathlib import Path
from typing import List
from app.models.history import HistoryItem
from app.core.logger import logger


class HistoryRepository:
    """
    Manages the persistence of conversation history in a local SQLite database.
    """

    def __init__(self, db_path: str = "chat_history.db"):
        """
        Initializes the repository and ensures the database and table exist.

        Args:
            db_path: The path to the SQLite database file.
        """
        self.db_path = Path(db_path)
        self._conn = None
        self._ensure_db_exists()

    def _get_connection(self):
        """Establishes and returns a database connection."""
        if self._conn is None:
            try:
                self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
                self._conn.row_factory = sqlite3.Row
            except sqlite3.Error as e:
                logger.error(f"Database connection error: {e}")
                raise
        return self._conn

    def _ensure_db_exists(self):
        """Creates the history table if it doesn't exist."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    item TEXT NOT NULL
                )
                """
            )
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to create history table: {e}")

    def add_interaction(self, item: HistoryItem):
        """
        Adds a user-bot interaction to the history.

        Args:
            item: A HistoryItem object representing the interaction.
        """
        conn = self._get_connection()
        item_json = item.model_dump_json()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO history (item) VALUES (?)", (item_json,))
            conn.commit()
        except sqlite3.Error as e:
            logger.error(f"Failed to add interaction to history: {e}")

    def get_history(self, limit: int = 50) -> List[HistoryItem]:
        """
        Retrieves the last N interactions from the history.

        Args:
            limit: The maximum number of interactions to retrieve.

        Returns:
            A list of HistoryItem objects.
        """
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT item FROM history ORDER BY id DESC LIMIT ?", (limit,)
            )
            rows = cursor.fetchall()
            # Reverse the order to maintain chronological sequence
            return [HistoryItem.model_validate_json(row["item"]) for row in reversed(rows)]
        except sqlite3.Error as e:
            logger.error(f"Failed to retrieve history: {e}")
            return []

    def clear_history(self):
        """Clears all interactions from the history."""
        conn = self._get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history")
            conn.commit()
            logger.info("Chat history cleared from the database.")
        except sqlite3.Error as e:
            logger.error(f"Failed to clear history: {e}")

    def __del__(self):
        """Ensures the database connection is closed on object destruction."""
        if self._conn:
            self._conn.close()
