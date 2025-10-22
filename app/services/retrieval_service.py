# -*- coding: utf-8 -*-
"""Service for retrieving relevant documents."""
from typing import List, Dict, Any
from app.repositories.chroma_repository import ChromaRepository


class RetrievalService:
    """Service for retrieving documents from the vector store."""

    def __init__(self):
        self.repository = ChromaRepository()

    def retrieve_documents(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant documents for a given query.

        Args:
            query: The query text.
            top_k: The number of documents to retrieve.

        Returns:
            A list of relevant documents.
        """
        return self.repository.query(query_text=query, top_k=top_k)

