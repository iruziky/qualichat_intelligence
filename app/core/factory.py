# -*- coding: utf-8 -*-
"""Factory for creating application components."""
from app.services.llm_service import LLMService
from app.services.embeddings_service import EmbeddingsService


class ServiceFactory:
    """Factory for creating services."""

    @staticmethod
    def create_llm_service(provider_name: str = "default") -> LLMService:
        """
        Create an LLM service.

        Args:
            provider_name: The name of the provider (e.g., 'openai', 'anthropic').

        Returns:
            An instance of LLMService.
        """
        # TODO: Implement dynamic provider selection
        return LLMService()

    @staticmethod
    def create_embeddings_service(provider_name: str = "default") -> EmbeddingsService:
        """
        Create an embeddings service.

        Args:
            provider_name: The name of the provider.

        Returns:
            An instance of EmbeddingsService.
        """
        # TODO: Implement dynamic provider selection
        return EmbeddingsService()
