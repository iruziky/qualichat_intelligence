# -*- coding: utf-8 -*-
"""Pydantic model for representing a text embedding."""
from typing import List
from pydantic import BaseModel


class Embedding(BaseModel):
    """
    Represents a vector embedding of a document.
    """

    vector: List[float]
    document_id: str
