# -*- coding: utf-8 -*-
"""Base class for all LangGraph graphs."""
from abc import ABC, abstractmethod
from langgraph.graph import StateGraph, END


class BaseGraph(ABC):
    """Base class for LangGraph implementations."""

    def __init__(self):
        self.workflow = StateGraph(self._get_initial_state())

    @abstractmethod
    def _get_initial_state(self) -> dict:
        """Define the initial state of the graph."""
        pass

    @abstractmethod
    def build(self):
        """Build the graph by adding nodes and edges."""
        pass

    def compile(self):
        """Compile the graph into a runnable app."""
        return self.workflow.compile()

