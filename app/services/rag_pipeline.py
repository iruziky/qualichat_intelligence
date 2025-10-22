# -*- coding: utf-8 -*-
"""Core RAG (Retrieval-Augmented Generation) pipeline."""
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService


class RAGPipeline:
    """Orchestrates the RAG pipeline."""

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.llm_service = LLMService()

    def execute(self, query: str) -> str:
        """
        Execute the RAG pipeline.

        Args:
            query: The user's query.

        Returns:
            The generated answer.
        """
        context_documents = self.retrieval_service.retrieve_documents(query)
        context = "\n".join(context_documents)

        prompt = f"""
        Context:
        {context}

        Question:
        {query}

        Answer:
        """

        messages = [{"role": "user", "content": prompt}]
        answer = self.llm_service.get_completion(messages)
        return answer

