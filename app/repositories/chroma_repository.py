# -*- coding: utf-8 -*-
"""Repository for interacting with ChromaDB."""
import chromadb
from typing import List, Optional

from app.core.config import settings
from app.repositories.base_repository import BaseRepository
from app.models.document import Document


class ChromaRepository(BaseRepository):
    """Repository for ChromaDB vector store."""

    def __init__(self, collection_name: str):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def add(self, documents: List[Document], embeddings: List[List[float]]):
        """
        Add documents and their embeddings to the ChromaDB collection.

        Args:
            documents: A list of Document objects.
            embeddings: A list of corresponding vector embeddings.
        """
        # Store source_name in metadata for filtering
        metadatas = []
        for doc in documents:
            meta = doc.metadata or {}
            meta["source_name"] = doc.source_name
            metadatas.append(meta)

        ids = [doc.id for doc in documents]

        self.collection.add(
            embeddings=embeddings,
            documents=[doc.content for doc in documents],
            metadatas=metadatas,
            ids=ids,
        )

    def query(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        source_name: Optional[str] = None,
    ) -> List[Document]:
        """
        Query the ChromaDB collection for similar documents.

        Args:
            query_embedding: The vector embedding of the query text.
            top_k: The number of results to return.
            source_name: Optional source name to filter the search.

        Returns:
            A list of Document objects that are similar to the query text.
        """
        where_clause = {}
        if source_name:
            where_clause = {"source_name": source_name}

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_clause,
        )

        documents = []
        if results and results["documents"]:
            for i, doc_content in enumerate(results["documents"][0]):
                doc_id = results["ids"][0][i]
                metadata = results["metadatas"][0][i]
                source = metadata.pop("source_name", "unknown")
                documents.append(
                    Document(
                        id=doc_id,
                        content=doc_content,
                        source_name=source,
                        metadata=metadata,
                    )
                )
        return documents

    def clear(self):
        """Clear all items from the collection."""
        self.collection.delete()

