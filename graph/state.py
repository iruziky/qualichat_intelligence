from typing import TypedDict, Annotated, List
import operator
from langchain_core.messages import AnyMessage

# Define o estado do grafo. Esta é a "memória" que será passada entre os nós.
class AgentState(TypedDict):
    # Histórico de mensagens da conversa
    messages: Annotated[list[AnyMessage], operator.add]
    
    # A pergunta do usuário, reformulada para maior clareza
    reformulated_query: str

    # Resultados da busca por similaridade
    search_results: List[str]
