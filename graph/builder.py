from langgraph.graph import StateGraph, END
from .state import AgentState
from .nodes.initial_request import process_initial_request

def build_graph():
    """
    Constrói o grafo de conversação.
    """
    workflow = StateGraph(AgentState)

    # Adiciona o nó que processa a requisição inicial
    workflow.add_node("initial_request", process_initial_request)

    # Define o ponto de entrada do grafo
    workflow.set_entry_point("initial_request")

    # Adiciona uma borda final para o nó initial_request
    workflow.add_edge("initial_request", END)

    # Compila o grafo
    return workflow.compile()