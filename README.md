# Qualichat Intelligence

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)

Backend inteligente projetado para potencializar o Qualichat com capacidades de IA conversacional avançada. Utiliza uma arquitetura de **Geração Aumentada por Recuperação (RAG)** orquestrada com **LangGraph** para criar fluxos de conversa com estado, modulares e eficientes.

---

## ✨ Core Features

- **Fluxo Conversacional com Estado:** Utiliza LangGraph para gerenciar o estado da conversa, permitindo interações mais complexas e contextuais.
- **Geração Aumentada por Recuperação (RAG):** Enriquece as respostas do LLM com informações de um banco de dados vetorial, garantindo respostas mais precisas e baseadas em conhecimento.
- **Suporte a Múltiplos LLMs e Embeddings:** Integrado com LiteLLM, permitindo a troca flexível entre diferentes provedores de modelos (OpenAI, Anthropic, etc.) através de configuração.
- **Persistência Vetorial Local:** Usa ChromaDB para armazenar e consultar embeddings de forma eficiente e local.
- **Gerenciamento Robusto:** Estruturado com Poetry para gerenciamento de dependências e Pydantic para validação de configurações.

---

## 🏛️ Arquitetura

O sistema opera com base em um pipeline RAG orquestrado. Quando uma pergunta é recebida, o fluxo é o seguinte:

1.  **Recuperação (RetrievalService):** A pergunta do usuário é transformada em um embedding vetorial. Esse embedding é usado para consultar o ChromaDB e encontrar os documentos ou trechos de conhecimento mais relevantes.
2.  **Enriquecimento (RAGPipeline):** Os documentos recuperados (contexto) são combinados com a pergunta original em um prompt otimizado.
3.  **Geração (LLMService):** O prompt enriquecido é enviado ao Large Language Model (LLM) para gerar uma resposta final, que é contextualizada e precisa.
4.  **Orquestração (ConversationGraph):** Todo o processo é gerenciado como um grafo de estados pelo LangGraph, garantindo um fluxo de dados claro e a capacidade de expandir o sistema com novos passos ou lógicas condicionais no futuro.

---

## 🚀 Getting Started

Siga os passos abaixo para configurar e executar o projeto localmente.

### Pré-requisitos

- Python 3.10+
- [Poetry](https://python-poetry.org/docs/#installation) para gerenciamento de dependências.

### 1. Instalação

Primeiro, clone o repositório e instale as dependências:

```bash
git clone <URL_DO_SEU_REPOSITORIO>
cd qualichat_intelligence
poetry install
```

### 2. Configuração do Ambiente

O projeto utiliza um arquivo `.env` para gerenciar chaves de API e outras configurações.

1.  Copie o arquivo de exemplo:
    ```bash
    cp .env.example .env
    ```

2.  Abra o arquivo `.env` e adicione sua chave de API do provedor de LLM. Atualmente, ele está configurado para a OpenAI:

    ```dotenv
    # .env
    OPENAI_API_KEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    DEFAULT_MODEL="gpt-4"
    VECTOR_DB_PATH="./chroma_db"
    ```

---

## ▶️ Usage

Para interagir com o assistente, utilize o terminal interativo. Ele permite testar o pipeline de conversação de ponta a ponta.

Execute o seguinte comando na raiz do projeto:

```bash
poetry run python run.py
```

O script será iniciado e você verá um prompt `>`. Simplesmente digite sua pergunta e pressione Enter. Para sair, digite `exit` ou `quit`.

---

## 📂 Estrutura do Projeto

```
qualichat_intelligence/
│
├── app/
│   ├── core/         # Configuração, logger e factories
│   ├── graphs/       # Lógica de orquestração com LangGraph
│   ├── models/       # Modelos de dados (Pydantic)
│   ├── repositories/ # Camada de acesso a dados (ChromaDB)
│   └── services/     # Lógica de negócio (LLM, Embeddings, RAG)
│
├── tests/            # Testes automatizados
├── .env.example      # Arquivo de exemplo para variáveis de ambiente
├── .gitignore        # Arquivos e pastas a serem ignorados pelo Git
├── pyproject.toml    # Definições do projeto e dependências (Poetry)
└── run.py            # Ponto de entrada para o terminal interativo
```

---

## 🗺️ Roadmap

- [ ] Implementar uma API (FastAPI) para expor o serviço de chat.
- [ ] Adicionar um serviço de ingestão de documentos para popular o ChromaDB.
- [ ] Expandir o `ConversationGraph` com mais nós para ferramentas e lógicas complexas.
- [ ] Criar um conjunto de testes unitários e de integração.

---

## 📄 Licença

Este projeto é licenciado sob a Licença MIT.