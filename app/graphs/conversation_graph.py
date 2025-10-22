# -*- coding: utf-8 -*-
"""Graph for managing conversations."""
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END

from app.graphs.base_graph import BaseGraph
from app.services.retrieval_service import RetrievalService
from app.services.rag_pipeline import RAGPipeline


class GraphState(TypedDict):
    """Represents the state of our graph."""
    question: str
    context: str
    answer: str


class ConversationGraph(BaseGraph):
    """Manages the conversational flow using LangGraph."""

    def __init__(self):
        super().__init__()
        self.retrieval_service = RetrievalService()
        self.rag_pipeline = RAGPipeline()

    def _get_initial_state(self) -> dict:
        return GraphState

    def retrieve_context(self, state):
        """Retrieve context from the vector store."""
        question = state["question"]
        context_documents = self.retrieval_service.retrieve_documents(question)
        context = "\n".join(context_documents)
        return {"context": context, "question": question}

    def generate_answer(self, state):
        """Generate an answer using the RAG pipeline."""
        question = state["question"]
        answer = self.rag_pipeline.execute(question)
        return {"answer": answer}

    def build(self):
        """Build the graph."""
        self.workflow.add_node("retrieve_context", self.retrieve_context)
        self.workflow.add_node("generate_answer", self.generate_answer)

        self.workflow.set_entry_point("retrieve_context")
        self.workflow.add_edge("retrieve_context", "generate_answer")
        self.workflow.add_edge("generate_answer", END)

