# -*- coding: utf-8 -*-
"""Repository for interacting with ChromaDB."""
import chromadb
from typing import List

from app.core.config import settings
from app.repositories.base_repository import BaseRepository
from app.services.embeddings_service import EmbeddingsService
from app.models.document import Document


class ChromaRepository(BaseRepository):
    """Repository for ChromaDB vector store."""

    def __init__(self, collection_name: str = "qualichat"):
        self.client = chromadb.PersistentClient(path=settings.VECTOR_DB_PATH)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.embeddings_service = EmbeddingsService()

    def add(self, documents: List[Document]):
        """
        Add documents to the ChromaDB collection.

        Args:
            documents: A list of Document objects.
        """
        texts = [doc.content for doc in documents]
        embeddings = self.embeddings_service.create_embeddings(texts)
        metadatas = [doc.metadata for doc in documents]
        ids = [doc.id for doc in documents]

        self.collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )

    def query(self, query_text: str, top_k: int = 5) -> List[Document]:
        """
        Query the ChromaDB collection for similar documents.

        Args:
            query_text: The text to search for.
            top_k: The number of results to return.

        Returns:
            A list of Document objects that are similar to the query text.
        """
        query_embedding = self.embeddings_service.create_embeddings([query_text])[0]
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )

        documents = []
        for i, doc_content in enumerate(results["documents"][0]):
            doc_id = results["ids"][0][i]
            metadata = results["metadatas"][0][i]
            documents.append(
                Document(id=doc_id, content=doc_content, metadata=metadata)
            )
        return documents

    def clear(self):
        """Clear all items from the collection."""
        self.collection.delete()

