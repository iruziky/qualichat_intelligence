# -*- coding: utf-8 -*-
"""Unit tests for the EmbeddingsService."""
from unittest.mock import patch, MagicMock

import pytest
from app.services.embeddings_service import EmbeddingsService


@patch("app.services.embeddings_service.embedding")
def test_create_embeddings_calls_litellm_and_parses_response(mock_litellm_embedding):
    """
    Test that create_embeddings correctly calls the litellm.embedding function
    and correctly parses the dictionary-based response.
    """
    # 1. Arrange: Configure the mock to return a predictable structure
    mock_embedding_data = [
        {"embedding": [0.1, 0.2, 0.3]},
        {"embedding": [0.4, 0.5, 0.6]},
    ]
    mock_response = MagicMock()
    mock_response.data = mock_embedding_data
    mock_litellm_embedding.return_value = mock_response

    # 2. Act: Call the method under test
    service = EmbeddingsService(model="test-embedding-model")
    texts_to_embed = ["hello world", "how are you?"]
    result_vectors = service.create_embeddings(texts_to_embed)

    # 3. Assert: Verify the behavior
    # Check that the litellm function was called with the correct arguments
    mock_litellm_embedding.assert_called_once_with(
        model="test-embedding-model", input=texts_to_embed
    )

    # Check that the response was parsed correctly into a list of vectors
    assert result_vectors == [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
