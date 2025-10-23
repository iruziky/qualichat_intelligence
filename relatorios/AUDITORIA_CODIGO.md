# Relatório de Auditoria de Código Detalhada: Qualichat Intelligence

## Visão Geral
Esta auditoria analisa cada arquivo do projeto para identificar violações de padrões de projeto, gambiarras, más práticas e riscos. A análise revelou uma arquitetura com boas intenções, mas com **violações significativas do padrão de Injeção de Dependência e da separação de camadas**, resultando em alto acoplamento e dificultando a testabilidade e manutenção.

---

### Arquivo: `run.py`

- **Linha(s):** 4-8
  - **Tipo:** Gambiarra / Má Prática
  - **Descrição:** O patch de compatibilidade do `sqlite3` está duplicado. Este código é crítico para o funcionamento do ChromaDB no ambiente atual, mas sua presença em múltiplos scripts (`run.py`, `ingest.py`) viola o princípio DRY.
  - **Sugestão:** Centralizar o patch em um único arquivo (`app/core/patches.py`) e importá-lo no início de cada ponto de entrada.

- **Linha(s):** 12
  - **Tipo:** Má Prática
  - **Descrição:** A variável `SOURCE_DOCUMENT` está "hardcoded" para fins de teste. Isso é perigoso, pois pode ser esquecido e enviado para produção, fazendo com que o sistema opere em um subconjunto de dados inesperadamente.
  - **Sugestão:** Mover essa lógica para um argumento de linha de comando ou carregá-la de uma variável de ambiente de desenvolvimento, deixando claro que é uma configuração de depuração.

- **Linha(s):** 23
  - **Tipo:** Violação de Design Pattern (Injeção de Dependência)
  - **Descrição:** O `HistoryRepository` e o `ConversationGraph` são instanciados diretamente (`history_repo = HistoryRepository()`, `graph = ConversationGraph()`). Isso acopla o `main` às implementações concretas, dificultando testes e a substituição de componentes.
  - **Sugestão:** Utilizar uma `Factory` para construir e fornecer todas as dependências necessárias para o `main`, aplicando o padrão de Injeção de Dependência.

- **Linha(s):** 61
  - **Tipo:** Risco / Má Prática
  - **Descrição:** O bloco `except Exception as e:` é muito genérico. Ele captura qualquer erro possível, o que pode mascarar bugs específicos e dificultar a depuração.
  - **Sugestão:** Capturar exceções mais específicas (ex: `FileNotFoundError`, `ValidationError` da Pydantic) para fornecer feedback mais claro ao usuário e logs mais precisos.

---

### Arquivo: `ingest.py`

- **Linha(s):** 5-9
  - **Tipo:** Gambiarra / Má Prática
  - **Descrição:** Mesma duplicação do patch do `sqlite3` encontrada em `run.py`.
  - **Sugestão:** Centralizar o patch.

- **Linha(s):** 21
  - **Tipo:** Violação de Design Pattern (Injeção de Dependência)
  - **Descrição:** O `IngestionService` é instanciado diretamente.
  - **Sugestão:** Usar a `Factory` para criar a instância do serviço.

---

### Arquivo: `app/core/document_factory.py`

- **Linha(s):** 22
  - **Tipo:** Má Prática
  - **Descrição:** Os parâmetros `chunk_size` e `chunk_overlap` estão "hardcoded" com valores padrão.
  - **Sugestão:** Mover esses valores para o arquivo de configuração central (`app/core/config.py`) para que possam ser gerenciados externamente.

- **Linha(s):** 69
  - **Tipo:** Risco / Má Prática
  - **Descrição:** Uso de `except Exception as e:`, que é muito genérico.
  - **Sugestão:** Capturar exceções específicas dos loaders da LangChain ou de operações de arquivo.

---

### Arquivo: `app/core/factory.py`

- **Análise Geral:** O arquivo está bem implementado e cumpre seu propósito. No entanto, ele está **subutilizado**, pois o restante do código raramente o usa, preferindo a instanciação direta (ver violações de DI em outros arquivos). A factory também poderia ser expandida para gerenciar a injeção de dependências de forma mais completa.

---

### Arquivo: `app/graphs/conversation_graph.py`

- **Linha(s):** 27-28
  - **Tipo:** Violação de Design Pattern (Injeção de Dependência)
  - **Descrição:** `RetrievalService` e `RAGPipeline` são instanciados diretamente no construtor. Isso cria um forte acoplamento entre o grafo e as implementações concretas dos serviços. O grafo não deveria saber como construir suas dependências.
  - **Sugestão:** Modificar o construtor para **receber** as instâncias dos serviços como argumentos (ex: `__init__(self, retrieval_service: RetrievalService, rag_pipeline: RAGPipeline)`). A `Factory` seria então responsável por criar e "injetar" essas dependências.

---

### Arquivo: `app/repositories/chroma_repository.py`

- **Linha(s):** 17
  - **Tipo:** Violação Grave de Arquitetura de Camadas
  - **Descrição:** O `ChromaRepository` (camada de persistência) instancia e depende diretamente do `EmbeddingsService` (camada de serviço). Esta é uma inversão de dependência incorreta. A camada de repositório nunca deve depender da camada de serviço. A responsabilidade de gerar o embedding antes de salvar deveria ser de um serviço.
  - **Sugestão:** Refatorar o fluxo. Um serviço (ex: `IngestionService` ou um novo `StorageService`) deve chamar o `EmbeddingsService` para criar o vetor e, em seguida, passar o `Document` e o `Embedding` para o `ChromaRepository`, que teria a única responsabilidade de salvar os dados.

- **Linha(s):** 15
  - **Tipo:** Má Prática
  - **Descrição:** O nome da coleção `"qualichat"` está "hardcoded".
  - **Sugestão:** Mover para o arquivo de configuração.

---

### Arquivo: `app/repositories/history_repository.py`

- **Linha(s):** Todo o arquivo
  - **Tipo:** Risco / Má Prática
  - **Descrição:** A implementação baseada em JSON (lendo e reescrevendo o arquivo inteiro a cada interação) é ineficiente, não escalável e propensa a corrupção de dados em cenários concorrentes.
  - **Sugestão:** Substituir por um banco de dados `SQLite`. Isso forneceria transações ACID, performance muito superior e segurança contra corrupção de dados.

---

### Arquivo: `app/services/ingestion_service.py`

- **Linha(s):** 22-24
  - **Tipo:** Violação de Design Pattern (Injeção de Dependência)
  - **Descrição:** `DocumentRepository`, `ChromaRepository` e `DocumentFactory` são instanciados diretamente. O serviço está acoplado às suas dependências concretas.
  - **Sugestão:** Aplicar Injeção de Dependência: passar as instâncias dos repositórios e da factory como argumentos no construtor.

---

### Arquivo: `app/services/rag_pipeline.py`

- **Linha(s):** 14-15
  - **Tipo:** Violação de Design Pattern (Injeção de Dependência)
  - **Descrição:** `RetrievalService` e `LLMService` são instanciados diretamente.
  - **Sugestão:** Aplicar Injeção de Dependência no construtor.

---

### Arquivo: `app/services/retrieval_service.py`

- **Linha(s):** 12
  - **Tipo:** Violação de Design Pattern (Injeção de Dependência)
  - **Descrição:** `ChromaRepository` é instanciado diretamente.
  - **Sugestão:** Aplicar Injeção de Dependência no construtor.

---

### Arquivos sem Problemas Identificados
- `app/core/config.py`
- `app/core/logger.py`
- `app/graphs/base_graph.py`
- `app/models/document.py`
- `app/models/embedding.py`
- `app/models/history.py`
- `app/repositories/base_repository.py` (além da sugestão de renomeação)
- `app/repositories/document_repository.py`
- `app/services/embeddings_service.py`
- `app/services/llm_service.py`

---

## Conclusão e Recomendações Prioritárias

A auditoria revela que, embora as camadas estejam bem definidas estruturalmente, a **falha em aplicar consistentemente o padrão de Injeção de Dependência** é o problema arquitetural mais crítico. A instanciação direta de dependências em quase todas as classes de serviço e grafo criou um sistema fortemente acoplado, difícil de testar e manter.

**Ações Imediatas Recomendadas:**
1.  **Refatorar para Injeção de Dependência:** Modificar os construtores de todas as classes de serviço, grafo e repositório para receberem suas dependências, em vez de criá-las.
2.  **Expandir a Factory:** Fazer com que a `ServiceFactory` seja responsável por construir a árvore de dependências completa e fornecer as instâncias de alto nível (como `ConversationGraph` e `IngestionService`) já com tudo injetado.
3.  **Corrigir a Violação de Camada:** Mover a lógica de criação de embeddings para fora do `ChromaRepository`, fazendo com que um serviço orquestre a chamada ao `EmbeddingsService` e o salvamento no repositório.
4.  **Centralizar o Patch do `sqlite3`:** Eliminar a duplicação de código.
5.  **Substituir o `HistoryRepository`:** Migrar a persistência do histórico de JSON para SQLite.