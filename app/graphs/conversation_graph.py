# -*- coding: utf-8 -*-
"""Graph for managing conversations."""
from typing import List, Optional
from langgraph.graph import END
from langchain_core.messages import AIMessage

from app.graphs.base_graph import BaseGraph
from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from app.services.rag_pipeline import RAGPipeline
from app.models.history import HistoryItem
from graph.state import AgentState
from graph.nodes.initial_request import create_initial_request_node


class ConversationGraph(BaseGraph):
    """Manages the conversational flow using LangGraph."""

    def __init__(
        self,
        llm_service: LLMService,
        retrieval_service: RetrievalService,
        rag_pipeline: RAGPipeline,
    ):
        super().__init__()
        self.llm_service = llm_service
        self.retrieval_service = retrieval_service
        self.rag_pipeline = rag_pipeline

    def _get_initial_state(self) -> dict:
        return AgentState

    def retrieve_context(self, state):
        """Retrieve context from the vector store."""
        return {}

    def generate_answer(self, state):
        """Generate an answer using the RAG pipeline."""
        reformulated_query = state["reformulated_query"]
        search_results = state["search_results"]
        history = state.get("messages", [])
        answer = self.rag_pipeline.execute(reformulated_query, history=history)
        return {"messages": [AIMessage(content=answer)]}

    def build(self):
        """Build the graph."""
        initial_request_node = create_initial_request_node(
            self.llm_service, self.retrieval_service
        )
        self.workflow.add_node("initial_request", initial_request_node)
        self.workflow.add_node("generate_answer", self.generate_answer)

        self.workflow.set_entry_point("initial_request")
        self.workflow.add_edge("initial_request", "generate_answer")
        self.workflow.add_edge("generate_answer", END)
