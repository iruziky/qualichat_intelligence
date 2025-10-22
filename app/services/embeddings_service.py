# -*- coding: utf-8 -*-
"""Service for handling text embeddings."""
from litellm import embedding
from app.core.config import settings


class EmbeddingsService:
    """Service for generating text embeddings using LiteLLM."""

    def __init__(self, model: str = "text-embedding-ada-002"):
        self.model = model

    def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Create embeddings for a list of texts.

        Args:
            texts: A list of strings to be embedded.

        Returns:
            A list of embeddings, where each embedding is a list of floats.
        """
        response = embedding(model=self.model, input=texts)
        return [item.embedding for item in response.data]

