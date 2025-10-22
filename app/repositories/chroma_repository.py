# -*- coding: utf-8 -*-
"""Repository for interacting with ChromaDB."""
import chromadb
from typing import Any, List, Dict

from app.core.config import settings
from app.repositories.base_repository import BaseRepository
from app.services.embeddings_service import EmbeddingsService


class ChromaRepository(BaseRepository):
    """Repository for ChromaDB vector store."""

    def __init__(self, collection_name: str = "qualichat"):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embeddings_service = EmbeddingsService()

    def add(self, items: List[Dict[str, Any]]):
        """
        Add items to the ChromaDB collection.

        Args:
            items: A list of dictionaries, each with 'text' and 'metadata'.
        """
        texts = [item["text"] for item in items]
        embeddings = self.embeddings_service.create_embeddings(texts)
        metadatas = [item["metadata"] for item in items]
        ids = [str(hash(text)) for text in texts]

        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )

    def query(self, query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Query the ChromaDB collection for similar documents.

        Args:
            query_text: The text to search for.
            top_k: The number of results to return.

        Returns:
            A list of documents that are similar to the query text.
        """
        query_embedding = self.embeddings_service.create_embeddings([query_text])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
        return results["documents"][0]

    def clear(self):
        """Clear all items from the collection."""
        self.collection.delete()

