# -*- coding: utf-8 -*-
"""Core RAG (Retrieval-Augmented Generation) pipeline."""
from typing import List, Optional
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService
from app.models.history import HistoryItem


class RAGPipeline:
    """Orchestrates the RAG pipeline."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm_service: LLMService,
    ):
        self.retrieval_service = retrieval_service
        self.llm_service = llm_service

    def execute(
        self,
        query: str,
        history: List[HistoryItem] = None,
        source_name: Optional[str] = None,
    ) -> str:
        """
        Execute the RAG pipeline.

        Args:
            query: The user's query.
            history: A list of previous user/bot interactions.
            source_name: Optional source name to filter the document retrieval.

        Returns:
            The generated answer.
        """
        context_documents = self.retrieval_service.retrieve_documents(
            query, source_name=source_name
        )
        context = "\n".join([doc.content for doc in context_documents])

        prompt = f"""
        Based on the following context, answer the user's question.
        Context:
        {context}

        Question:
        {query}

        Answer:
        """

        messages = []
        if history:
            for interaction in history:
                messages.append({"role": "user", "content": interaction.user_message})
                messages.append(
                    {"role": "assistant", "content": interaction.bot_response}
                )

        messages.append({"role": "user", "content": prompt})
        answer = self.llm_service.get_completion(messages)
        return answer

