# -*- coding: utf-8 -*-
"""Service for interacting with Large Language Models."""
from litellm import completion
from app.core.config import settings


class LLMService:
    """Service to interact with LLMs using LiteLLM."""

    def __init__(self, model: str = None):
        self.model = model or settings.DEFAULT_MODEL

    def get_completion(self, messages: list[dict]) -> str:
        """
        Get a completion from the configured LLM.

        Args:
            messages: A list of messages in the format expected by LiteLLM.

        Returns:
            The content of the response message.
        """
        response = completion(model=self.model, messages=messages)
        return response.choices[0].message.content

