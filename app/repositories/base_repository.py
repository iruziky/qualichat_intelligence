# -*- coding: utf-8 -*-
"""Base class for all repositories."""
from abc import ABC, abstractmethod
from typing import Any, List, Dict


class BaseRepository(ABC):
    """Abstract base class for repositories."""

    @abstractmethod
    def add(self, items: List[Dict[str, Any]]):
        """Add items to the repository."""
        pass

    @abstractmethod
    def query(self, query_embedding: List[float], top_k: int) -> List[Dict[str, Any]]:
        """Query the repository for similar items."""
        pass

    @abstractmethod
    def clear(self):
        """Clear all items from the repository."""
        pass

