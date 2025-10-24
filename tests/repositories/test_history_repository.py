# -*- coding: utf-8 -*-
"""Unit tests for the HistoryRepository."""
import sqlite3
from pathlib import Path

import pytest
from app.models.history import HistoryItem
from app.repositories.history_repository import HistoryRepository


def test_history_repository_creates_db_file(tmp_path: Path):
    """Verify that the repository creates a new database file if it doesn't exist."""
    db_path = tmp_path / "history"
    db_path.mkdir()  # Ensure the parent directory exists
    repo = HistoryRepository(user_id="test_user", db_folder=str(db_path))
    assert (db_path / "user_test_user.db").exists()


def test_add_and_get_interaction(tmp_path: Path):
    """Test adding an interaction and retrieving it."""
    db_path = tmp_path / "history"
    db_path.mkdir()  # Ensure the parent directory exists
    repo = HistoryRepository(user_id="test_user", db_folder=str(db_path))

    # Add one item
    item1 = HistoryItem(user_message="Hello", bot_response="Hi there!")
    repo.add_interaction(item1)

    history = repo.get_history()
    assert len(history) == 1
    assert history[0].user_message == "Hello"
    assert history[0].bot_response == "Hi there!"

    # Add a second item
    item2 = HistoryItem(user_message="How are you?", bot_response="I am fine.")
    repo.add_interaction(item2)

    history = repo.get_history()
    assert len(history) == 2
    assert history[1].user_message == "How are you?"


def test_get_history_limit(tmp_path: Path):
    """Test the limit parameter of get_history."""
    db_path = tmp_path / "history"
    db_path.mkdir()  # Ensure the parent directory exists
    repo = HistoryRepository(user_id="test_user", db_folder=str(db_path))

    for i in range(10):
        item = HistoryItem(user_message=f"User {i}", bot_response=f"Bot {i}")
        repo.add_interaction(item)

    history = repo.get_history(limit=5)
    assert len(history) == 5
    assert history[0].user_message == "User 5"  # Chronological order is preserved
    assert history[4].user_message == "User 9"


def test_clear_history(tmp_path: Path):
    """Test clearing the history."""
    db_path = tmp_path / "history"
    db_path.mkdir()  # Ensure the parent directory exists
    repo = HistoryRepository(user_id="test_user", db_folder=str(db_path))

    item = HistoryItem(user_message="Test", bot_response="Test")
    repo.add_interaction(item)

    assert len(repo.get_history()) == 1

    repo.clear_history()
    assert len(repo.get_history()) == 0
