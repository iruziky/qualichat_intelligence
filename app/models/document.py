# -*- coding: utf-8 -*-
"""Pydantic model for representing a document."""
from typing import Optional, Dict, Any
from pydantic import BaseModel


class Document(BaseModel):
    """
    Represents a piece of content to be stored and retrieved.
    """

    id: str
    content: str
    source_name: str
    metadata: Optional[Dict[str, Any]] = None
