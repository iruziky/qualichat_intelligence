# -*- coding: utf-8 -*-
"""Factory for creating and composing application components."""

from app.services.llm_service import LLMService
from app.services.embeddings_service import EmbeddingsService
from app.services.retrieval_service import RetrievalService
from app.services.rag_pipeline import RAGPipeline
from app.services.ingestion_service import IngestionService
from app.repositories.history_repository import HistoryRepository
from app.repositories.chroma_repository import ChromaRepository
from app.repositories.document_repository import DocumentRepository
from app.graphs.conversation_graph import ConversationGraph
from app.core.document_factory import DocumentFactory


class AppFactory:
    """
    Acts as the Composition Root for the application.
    Creates and wires together all the components of the system.
    """

    @staticmethod
    def create_llm_service() -> LLMService:
        return LLMService()

    @staticmethod
    def create_embeddings_service() -> EmbeddingsService:
        return EmbeddingsService()

    @staticmethod
    def create_chroma_repository() -> ChromaRepository:
        return ChromaRepository()

    @staticmethod
    def create_history_repository() -> HistoryRepository:
        return HistoryRepository()

    @staticmethod
    def create_document_repository() -> DocumentRepository:
        return DocumentRepository()

    @staticmethod
    def create_document_factory() -> DocumentFactory:
        return DocumentFactory()

    @classmethod
    def create_retrieval_service(cls) -> RetrievalService:
        return RetrievalService(
            repository=cls.create_chroma_repository(),
            embeddings_service=cls.create_embeddings_service(),
        )

    @classmethod
    def create_rag_pipeline(cls) -> RAGPipeline:
        return RAGPipeline(
            retrieval_service=cls.create_retrieval_service(),
            llm_service=cls.create_llm_service(),
        )

    @classmethod
    def create_conversation_graph(cls) -> ConversationGraph:
        graph = ConversationGraph(
            retrieval_service=cls.create_retrieval_service(),
            rag_pipeline=cls.create_rag_pipeline(),
        )
        graph.build()
        return graph.compile()

    @classmethod
    def create_ingestion_service(cls, user_id: str) -> IngestionService:
        return IngestionService(
            user_id=user_id,
            document_repo=cls.create_document_repository(),
            chroma_repo=cls.create_chroma_repository(),
            doc_factory=cls.create_document_factory(),
            embeddings_service=cls.create_embeddings_service(),
        )
