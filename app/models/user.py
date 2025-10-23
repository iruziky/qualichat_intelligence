# -*- coding: utf-8 -*-
"""Domain entity representing a User."""
from typing import List
from pathlib import Path

from app.models.history import HistoryItem
from app.repositories.history_repository import HistoryRepository
from app.repositories.document_repository import DocumentRepository


class User:
    """
    Represents a user, providing an interface to their documents and history.
    """

    def __init__(
        self,
        user_id: str,
        history_repo: HistoryRepository,
        document_repo: DocumentRepository,
    ):
        self.id = user_id
        self._history_repo = history_repo
        self._document_repo = document_repo

    def get_history(self, limit: int = 50) -> List[HistoryItem]:
        """Retrieves the user's conversation history."""
        return self._history_repo.get_history(limit)

    def add_interaction(self, user_message: str, bot_response: str):
        """Adds a new interaction to the user's history."""
        item = HistoryItem(user_message=user_message, bot_response=bot_response)
        self._history_repo.add_interaction(item)

    def clear_history(self):
        """Clears the user's conversation history."""
        self._history_repo.clear_history()

    def get_documents(self) -> List[Path]:
        """Retrieves the user's source documents."""
        return self._document_repo.get_user_documents(self.id)
