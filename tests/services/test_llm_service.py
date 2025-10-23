# -*- coding: utf-8 -*-
"""Unit tests for the LLMService."""
from unittest.mock import patch, MagicMock

import pytest
from app.services.llm_service import LLMService


@patch("app.services.llm_service.completion")
def test_llm_service_get_completion(mock_litellm_completion):
    """
    Test that get_completion correctly calls the litellm library
    and extracts the content from the response.
    """
    # 1. Arrange: Configure the mock to return a predictable structure
    mock_response = MagicMock()
    mock_choice = MagicMock()
    mock_message = MagicMock()
    mock_message.content = "This is the mocked LLM response."
    mock_choice.message = mock_message
    mock_response.choices = [mock_choice]
    mock_litellm_completion.return_value = mock_response

    # 2. Act: Call the method under test
    service = LLMService(model="gpt-test")
    messages = [{"role": "user", "content": "Hello"}]
    result = service.get_completion(messages)

    # 3. Assert: Verify the behavior
    # Check that the litellm function was called correctly
    mock_litellm_completion.assert_called_once_with(
        model="gpt-test", messages=messages
    )
    # Check that the response was parsed correctly
    assert result == "This is the mocked LLM response."
