# -*- coding: utf-8 -*-
"""Unit tests for the DocumentRepository."""
from pathlib import Path

import pytest
from app.repositories.document_repository import DocumentRepository


def test_get_user_documents(tmp_path: Path):
    """Test listing documents for a user, including ignoring hidden files."""
    base_path = tmp_path / "documents"
    user_path = base_path / "test_user"
    user_path.mkdir(parents=True)

    # Create some files
    (user_path / "doc1.txt").touch()
    (user_path / "doc2.pdf").touch()
    (user_path / ".hidden_file").touch()  # Should be ignored
    (user_path / "subfolder").mkdir()     # Should be ignored

    repo = DocumentRepository(base_path=str(base_path))
    documents = repo.get_user_documents(user_id="test_user")

    assert len(documents) == 2
    doc_names = {doc.name for doc in documents}
    assert "doc1.txt" in doc_names
    assert "doc2.pdf" in doc_names
    assert ".hidden_file" not in doc_names


def test_get_documents_for_nonexistent_user(tmp_path: Path):
    """Test that an empty list is returned for a user with no directory."""
    base_path = tmp_path / "documents"
    repo = DocumentRepository(base_path=str(base_path))
    documents = repo.get_user_documents(user_id="nonexistent_user")
    assert documents == []
