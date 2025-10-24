# -*- coding: utf-8 -*-
"""Core RAG (Retrieval-Augmented Generation) pipeline."""
from typing import List, Optional
from app.services.retrieval_service import RetrievalService
from app.services.llm_service import LLMService


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
        history: List = None,
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
            from langchain_core.messages import HumanMessage

            for interaction in history:
                if isinstance(interaction, HumanMessage):
                    messages.append({"role": "user", "content": interaction.content})
                else:  # Assumes AIMessage
                    messages.append(
                        {"role": "assistant", "content": interaction.content}
                    )

        messages.append({"role": "user", "content": prompt})
        answer = self.llm_service.get_completion(messages)
        return answer

