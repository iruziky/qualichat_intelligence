# Relatório de Auditoria Focada: Padrões de Projeto e Arquitetura

## Visão Geral
Esta auditoria focada analisa a implementação dos padrões **Factory, Repository e Model Layer**, identificando violações de responsabilidade, acoplamento indevido e falhas na aplicação de **Injeção de Dependência (DI)**. A análise confirma que a estrutura de camadas existe, mas é minada por um **forte acoplamento** causado pela instanciação direta de dependências, o que representa o maior risco arquitetural do projeto.

---

### Arquivo: `run.py` (Ponto de Entrada)

- **Linha(s):** 23, 24
- **Tipo:** Violação Grave de Design Pattern (Injeção de Dependência)
- **Descrição:** `HistoryRepository` e `ConversationGraph` são instanciados diretamente (`history_repo = HistoryRepository()`). O ponto de entrada da aplicação está fortemente acoplado às implementações concretas de seus componentes principais. Isso impede a testabilidade (não é possível "mockar" o grafo ou o repositório) e a flexibilidade.
- **Sugestão:** O `main` deveria receber suas dependências de uma camada de composição (um "Composition Root"), que seria o único lugar onde a `Factory` é usada para construir a árvore de objetos.

---

### Arquivo: `ingest.py` (Ponto de Entrada)

- **Linha(s):** 21
- **Tipo:** Violação Grave de Design Pattern (Injeção de Dependência)
- **Descrição:** `IngestionService` é instanciado diretamente. Mesma violação encontrada em `run.py`.
- **Sugestão:** Utilizar a `Factory` para construir e fornecer a instância do `IngestionService`.

---

### Arquivo: `app/core/factory.py` (Factory Pattern)

- **Análise Geral:** A `ServiceFactory` existe, mas está **subutilizada e incompleta**. Ela cria apenas alguns componentes de forma isolada e não gerencia a **injeção de dependências** entre eles. Uma Factory robusta deveria ser capaz de construir um objeto complexo (como o `ConversationGraph`) com todas as suas dependências já resolvidas e injetadas.
- **Sugestão:** A `Factory` deveria ser o "orquestrador" da construção de objetos. Por exemplo, `create_conversation_graph()` deveria instanciar internamente o `RAGPipeline` e o `RetrievalService` (que por sua vez teriam suas dependências injetadas) e passá-los para o construtor do `ConversationGraph`.

---

### Arquivo: `app/core/document_factory.py`

- **Análise Geral:** O nome "Factory" aqui é usado no sentido de "criador de objetos", não no padrão de DI. A implementação está correta para sua finalidade: encapsula a lógica de criação de `Document` a partir de arquivos.
- **Pontos de Melhoria (Má Prática):**
    - **Linha 22:** `chunk_size` e `chunk_overlap` estão "hardcoded", violando o princípio de configuração externa.
    - **Sugestão:** Mover para `app/core/config.py` e injetá-los no construtor da `DocumentFactory`.

---

### Arquivos: `app/models/*.py` (Model Layer)

- **Análise Geral:** **Implementação Correta.** Todos os modelos (`HistoryItem`, `Document`, `Embedding`) cumprem perfeitamente sua responsabilidade. Eles contêm apenas a definição da estrutura de dados, tipos e validações, sem qualquer lógica de negócio ou persistência.

---

### Arquivo: `app/repositories/chroma_repository.py` (Repository Pattern)

- **Linha(s):** 17
- **Tipo:** Violação Gravíssima de Arquitetura de Camadas
- **Descrição:** O `ChromaRepository` (camada de dados) instancia e depende do `EmbeddingsService` (camada de serviço). Esta é a violação mais crítica encontrada. **Um repositório NUNCA deve depender de um serviço.** Sua única responsabilidade é interagir com a fonte de dados (neste caso, ChromaDB). A lógica de negócio (como gerar um embedding) pertence à camada de serviço.
- **Sugestão:** A responsabilidade de gerar embeddings deve ser movida para a camada de serviço. O fluxo correto seria:
    1. Um serviço (ex: `IngestionService`) recebe um `Document`.
    2. O serviço chama o `EmbeddingsService` para obter o vetor.
    3. O serviço passa o `Document` e o vetor para o `ChromaRepository`, cujos métodos `add` e `query` deveriam aceitar os embeddings diretamente, em vez de calculá-los.

---

### Arquivo: `app/repositories/history_repository.py` (Repository Pattern)

- **Análise Geral:** **Implementação Correta do Padrão.** O repositório abstrai com sucesso a lógica de persistência (leitura/escrita de JSON). Ele não tem dependências indevidas e cumpre sua responsabilidade única.
- **Ponto de Risco (Implementação):** A escolha de JSON como backend é uma **má prática** para qualquer aplicação que não seja um protótipo simples, devido à ineficiência e falta de segurança contra concorrência.

---

### Arquivo: `app/repositories/document_repository.py` (Repository Pattern)

- **Análise Geral:** **Implementação Correta do Padrão.** Abstrai perfeitamente o acesso ao sistema de arquivos para buscar documentos, tratando-o como uma fonte de dados.

---

### Arquivos: `app/services/*.py` (Service Layer)

- **Análise Geral:** Todos os serviços (`IngestionService`, `RAGPipeline`, `RetrievalService`) violam o padrão de Injeção de Dependência.
- **Tipo:** Violação de Design Pattern (Injeção de Dependência)
- **Descrição:** Em cada serviço, suas dependências (outros serviços ou repositórios) são instanciadas diretamente nos construtores.
    - `IngestionService` (linhas 22-24) cria `DocumentRepository`, `ChromaRepository`, `DocumentFactory`.
    - `RAGPipeline` (linhas 14-15) cria `RetrievalService`, `LLMService`.
    - `RetrievalService` (linha 12) cria `ChromaRepository`.
- **Sugestão:** Aplicar Injeção de Dependência em todos os serviços. Os construtores devem **receber** as instâncias de suas dependências.

---

### Arquivo: `app/graphs/conversation_graph.py`

- **Linha(s):** 27-28
- **Tipo:** Violação de Design Pattern (Injeção de Dependência)
- **Descrição:** O grafo, que deveria apenas orquestrar a lógica, está fortemente acoplado à criação de suas dependências (`RetrievalService`, `RAGPipeline`).
- **Sugestão:** Aplicar Injeção de Dependência no construtor, recebendo as instâncias dos serviços.

---

## Conclusão Final da Auditoria

A arquitetura do projeto está em um estado **crítico, mas corrigível**. A estrutura de arquivos e a intenção de separar as camadas são boas, mas a falha sistemática em aplicar a **Injeção de Dependência** e a **violação de responsabilidade no `ChromaRepository`** anulam os benefícios da modularidade, criando um sistema monolítico disfarçado de arquitetura em camadas.

**Ações Corretivas Mandatórias:**
1.  **Refatorar para Injeção de Dependência (DI) em toda a aplicação:** Nenhum serviço, grafo ou repositório deve instanciar suas próprias dependências. Elas devem ser passadas via construtor.
2.  **Corrigir a Violação de Camada no `ChromaRepository`:** Mover a responsabilidade de gerar embeddings para a camada de serviço.
3.  **Expandir a `Factory`:** Torná-la o "Composition Root" da aplicação, responsável por construir e conectar todos os componentes.
4.  **Substituir a persistência do `HistoryRepository` para SQLite.**
5.  **Centralizar o patch do `sqlite3` e as configurações "hardcoded".**
