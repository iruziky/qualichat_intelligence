# -*- coding: utf-8 -*-
"""Repository for persisting chat history."""
import json
from pathlib import Path
from typing import List
from app.models.history import HistoryItem


class HistoryRepository:
    """
    Manages the persistence of conversation history in a local JSON file.
    """

    def __init__(self, db_path: str = "chat_history.json"):
        """
        Initializes the repository and ensures the database file exists.

        Args:
            db_path: The path to the JSON file used for storage.
        """
        self.db_path = Path(db_path)
        self._ensure_db_exists()

    def _ensure_db_exists(self):
        """Creates the JSON history file if it doesn't exist."""
        if not self.db_path.exists():
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _read_history(self) -> List[HistoryItem]:
        """Reads the entire history from the JSON file."""
        with open(self.db_path, "r", encoding="utf-8") as f:
            try:
                history_data = json.load(f)
                return [HistoryItem.model_validate(item) for item in history_data]
            except json.JSONDecodeError:
                return []

    def _write_history(self, history: List[HistoryItem]):
        """Writes the entire history to the JSON file."""
        history_data = [item.model_dump(mode="json") for item in history]
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(history_data, f, indent=2, ensure_ascii=False)

    def add_interaction(self, item: HistoryItem):
        """
        Adds a user-bot interaction to the history.

        Args:
            item: A HistoryItem object representing the interaction.
        """
        history = self._read_history()
        history.append(item)
        self._write_history(history)

    def get_history(self, limit: int = 50) -> List[HistoryItem]:
        """
        Retrieves the last N interactions from the history.

        Args:
            limit: The maximum number of interactions to retrieve.

        Returns:
            A list of HistoryItem objects.
        """
        history = self._read_history()
        return history[-limit:]

    def clear_history(self):
        """Clears all interactions from the history."""
        self._write_history([])
