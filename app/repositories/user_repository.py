# -*- coding: utf-8 -*-
"""Repository responsible for creating and retrieving User objects."""

from app.models.user import User
from app.repositories.history_repository import HistoryRepository
from app.repositories.document_repository import DocumentRepository


class UserRepository:
    """
    Acts as a factory to construct User domain objects.
    """

    def __init__(self, document_repo: DocumentRepository):
        self._document_repo = document_repo

    def get_by_id(self, user_id: str) -> User:
        """
        Gets a User object by their ID.

        This method constructs the user object with its specific dependencies.

        Args:
            user_id: The ID of the user to retrieve.

        Returns:
            A fully constructed User object.
        """
        # Instantiate the user-specific history repository
        history_repo = HistoryRepository(user_id=user_id)

        # Construct the User object with its dependencies
        return User(
            user_id=user_id,
            history_repo=history_repo,
            document_repo=self._document_repo,
        )
