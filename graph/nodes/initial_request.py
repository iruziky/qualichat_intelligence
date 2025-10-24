from typing import Dict, Any, List
from functools import partial
from langchain_core.messages import HumanMessage, AnyMessage

from app.services.llm_service import LLMService
from app.services.retrieval_service import RetrievalService
from ..state import AgentState


def get_last_user_message(messages: List[AnyMessage]) -> str:
    """
    Extrai o conteúdo da última mensagem do usuário (HumanMessage) do histórico.
    """
    if not messages or not isinstance(messages[-1], HumanMessage):
        raise ValueError("A última mensagem não é do usuário (HumanMessage).")
    return messages[-1].content


def reformulate_query(llm_service: LLMService, query: str) -> str:
    """
    Usa um LLM para reformular a pergunta do usuário, tornando-a mais clara e direta
    para a busca por similaridade.
    """
    prompt = f"""Sua tarefa é reformular a consulta de um usuário para que ela seja mais eficaz em uma busca por similaridade em uma base de documentos.
    - Se a consulta for uma saudação ou uma interação social curta (como "oi", "olá", "tudo bem?"), transforme-a em uma descrição da ação do usuário.
    - Se a consulta for uma pergunta real, reformule-a para ser mais clara, direta e completa, otimizando-a para a busca.
    - Retorne apenas a consulta reformulada, sem adicionar nenhuma outra frase ou explicação.

    Exemplos:
    - Consulta Original: "oi"
      Consulta Reformulada: "Usuário fez uma abordagem inicial mandando um 'oi'"
    - Consulta Original: "como funciona a liberação do crédito?"
      Consulta Reformulada: "Explique o processo de liberação de crédito do consórcio."
    - Consulta Original: "quais os docs pra liberar?"
      Consulta Reformulada: "Quais são os documentos necessários para a liberação do crédito?"

    Agora, reformule a seguinte consulta:

    Consulta Original: "{query}"
    """
    response = llm_service.get_completion([{"role": "user", "content": prompt}])
    return response


def similarity_search(
    retrieval_service: RetrievalService, query: str
) -> list[str]:
    """
    Realiza uma busca por similaridade no ChromaDB.
    """
    documents = retrieval_service.retrieve_documents(query, top_k=3)
    return [doc.content for doc in documents]


def process_initial_request(
    state: AgentState, llm_service: LLMService, retrieval_service: RetrievalService
) -> Dict[str, Any]:
    """
    Nó que processa a requisição inicial do usuário.
    1. Pega a última mensagem do usuário.
    2. Reformula a mensagem para maior clareza.
    3. Realiza uma busca por similaridade.
    """
    print("--- Executando Nó: process_initial_request ---")

    # 1. Pega a última mensagem do usuário
    user_query = get_last_user_message(state["messages"])
    print(f"Query Original: {user_query}")

    # 2. Reformula a mensagem
    reformulated = reformulate_query(llm_service, user_query)
    print(f"Query Reformulada: {reformulated}")

    # 3. Realiza a busca por similaridade
    search_results = similarity_search(retrieval_service, reformulated)
    print(f"Resultados da Busca: {search_results}")

    # Retorna os novos valores para serem adicionados ao estado
    return {
        "reformulated_query": reformulated,
        "search_results": search_results,
    }


def create_initial_request_node(
    llm_service: LLMService, retrieval_service: RetrievalService
):
    """
    Cria um nó de requisição inicial com os serviços injetados.
    """
    return partial(
        process_initial_request,
        llm_service=llm_service,
        retrieval_service=retrieval_service,
    )