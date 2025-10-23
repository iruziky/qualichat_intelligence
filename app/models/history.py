# -*- coding: utf-8 -*-
"""Pydantic model for representing a single interaction in the chat history."""
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field


class HistoryItem(BaseModel):
    """
    Represents a single user-bot interaction.
    """

    user_message: str
    bot_response: str
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
