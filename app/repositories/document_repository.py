# -*- coding: utf-8 -*-
"""Repository for accessing source documents from the file system."""
from pathlib import Path
from typing import List

from app.core.logger import logger


class DocumentRepository:
    """
    Simulates access to a database of source documents stored on the file system.
    """

    def __init__(self, base_path: str = "documents"):
        """
        Initializes the repository with the base path for documents.

        Args:
            base_path: The root directory where user documents are stored.
        """
        self.base_path = Path(base_path)
        if not self.base_path.exists():
            logger.warning(
                f"Base document path '{self.base_path}' does not exist. Creating it."
            )
            self.base_path.mkdir(parents=True, exist_ok=True)

    def get_user_documents(self, user_id: str) -> List[Path]:
        """
        Lists all document file paths for a given user.

        Args:
            user_id: The ID of the user (which corresponds to a subdirectory).

        Returns:
            A list of Path objects for each document found.
        """
        user_path = self.base_path / user_id
        if not user_path.is_dir():
            logger.warning(f"No document directory found for user: {user_id}")
            return []

        # Return a list of all files, excluding directories and hidden files
        return [
            file
            for file in user_path.iterdir()
            if file.is_file() and not file.name.startswith(".")
        ]
