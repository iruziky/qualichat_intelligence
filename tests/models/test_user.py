# -*- coding: utf-8 -*-
"""Unit tests for the User domain entity."""
from unittest.mock import MagicMock

import pytest
from app.models.user import User


@pytest.fixture
def mock_repos():
    """Fixture to create mock repositories for the User entity."""
    history_repo = MagicMock()
    doc_repo = MagicMock()
    return history_repo, doc_repo


def test_user_get_history(mock_repos):
    """Test that get_history correctly calls the underlying repository."""
    history_repo, doc_repo = mock_repos
    user = User(user_id="test_user", history_repo=history_repo, document_repo=doc_repo)

    user.get_history(limit=10)
    history_repo.get_history.assert_called_once_with(10)


def test_user_add_interaction(mock_repos):
    """Test that add_interaction correctly calls the underlying repository."""
    history_repo, doc_repo = mock_repos
    user = User(user_id="test_user", history_repo=history_repo, document_repo=doc_repo)

    user.add_interaction(user_message="Hi", bot_response="Hello")
    # Verifies that the method was called, without being too strict on the object instance
    assert history_repo.add_interaction.call_count == 1
    # Optional: more detailed check on the content
    call_args = history_repo.add_interaction.call_args[0][0]
    assert call_args.user_message == "Hi"
    assert call_args.bot_response == "Hello"


def test_user_get_documents(mock_repos):
    """Test that get_documents correctly calls the underlying repository."""
    history_repo, doc_repo = mock_repos
    user = User(user_id="test_user", history_repo=history_repo, document_repo=doc_repo)

    user.get_documents()
    doc_repo.get_user_documents.assert_called_once_with("test_user")
