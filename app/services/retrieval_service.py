# -*- coding: utf-8 -*-
"""Service for retrieving relevant documents."""
from typing import List, Optional
from app.repositories.chroma_repository import ChromaRepository
from app.models.document import Document


class RetrievalService:
    """Service for retrieving documents from the vector store."""

    def __init__(self):
        self.repository = ChromaRepository()

    def retrieve_documents(
        self, query: str, top_k: int = 5, source_name: Optional[str] = None
    ) -> List[Document]:
        """
        Retrieve relevant documents for a given query.

        Args:
            query: The query text.
            top_k: The number of documents to retrieve.
            source_name: Optional source name to filter the search.

        Returns:
            A list of relevant Document objects.
        """
        return self.repository.query(
            query_text=query, top_k=top_k, source_name=source_name
        )

