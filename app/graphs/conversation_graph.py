# -*- coding: utf-8 -*-
"""Graph for managing conversations."""
from typing import TypedDict, List, Optional
from langgraph.graph import StateGraph, END

from app.graphs.base_graph import BaseGraph
from app.services.retrieval_service import RetrievalService
from app.services.rag_pipeline import RAGPipeline
from app.models.history import HistoryItem


class GraphState(TypedDict):
    """Represents the state of our graph."""
    question: str
    context: str
    answer: str
    history: List[HistoryItem]
    source_name: Optional[str]


class ConversationGraph(BaseGraph):
    """Manages the conversational flow using LangGraph."""

    def __init__(
        self,
        retrieval_service: RetrievalService,
        rag_pipeline: RAGPipeline,
    ):
        super().__init__()
        self.retrieval_service = retrieval_service
        self.rag_pipeline = rag_pipeline

    def _get_initial_state(self) -> dict:
        return GraphState

    def retrieve_context(self, state):
        """Retrieve context from the vector store."""
        question = state["question"]
        history = state.get("history", [])
        source_name = state.get("source_name")
        context_documents = self.retrieval_service.retrieve_documents(
            question, source_name=source_name
        )
        context = "\n".join([doc.content for doc in context_documents])
        return {
            "context": context,
            "question": question,
            "history": history,
            "source_name": source_name,
        }

    def generate_answer(self, state):
        """Generate an answer using the RAG pipeline."""
        question = state["question"]
        history = state.get("history", [])
        source_name = state.get("source_name")
        answer = self.rag_pipeline.execute(
            question, history=history, source_name=source_name
        )
        return {"answer": answer}

    def build(self):
        """Build the graph."""
        self.workflow.add_node("retrieve_context", self.retrieve_context)
        self.workflow.add_node("generate_answer", self.generate_answer)

        self.workflow.set_entry_point("retrieve_context")
        self.workflow.add_edge("retrieve_context", "generate_answer")
        self.workflow.add_edge("generate_answer", END)


