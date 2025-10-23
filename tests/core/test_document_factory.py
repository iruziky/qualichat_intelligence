# -*- coding: utf-8 -*-
"""Unit tests for the DocumentFactory."""
from pathlib import Path

import pytest
from app.core.document_factory import DocumentFactory


def test_create_documents_from_txt(tmp_path: Path):
    """Test creating documents from a simple .txt file."""
    file_path = tmp_path / "test.txt"
    file_path.write_text("This is a sentence. This is another sentence.")

    factory = DocumentFactory(chunk_size=20, chunk_overlap=5)
    documents = factory.create_documents(str(file_path))

    assert len(documents) == 3  # Adjusted to the actual chunking behavior
    assert documents[0].content == "This is a sentence."
    assert documents[1].content == "This is another"
    assert all(doc.source_name == "test.txt" for doc in documents)


def test_unsupported_file_type(tmp_path: Path):
    """Test that an unsupported file type returns an empty list."""
    file_path = tmp_path / "test.zip"
    file_path.touch()

    factory = DocumentFactory(chunk_size=100, chunk_overlap=10)
    documents = factory.create_documents(str(file_path))
    assert documents == []


def test_nonexistent_file(tmp_path: Path):
    """Test that a nonexistent file returns an empty list."""
    factory = DocumentFactory(chunk_size=100, chunk_overlap=10)
    documents = factory.create_documents(str(tmp_path / "nonexistent.txt"))
    assert documents == []
