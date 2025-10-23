# -*- coding: utf-8 -*-
"""Integration test for the full RAG pipeline."""
import app  # Import the top-level package for robust patching
from pathlib import Path
from unittest.mock import patch

import pytest
from app.core.factory import AppFactory


@pytest.fixture
def setup_rag_environment(tmp_path: Path, monkeypatch):
    """
    Set up a temporary, isolated environment for RAG integration tests.
    - Creates temporary directories for documents, history, and the vector DB.
    - Mocks settings and repository constructors to use these temporary paths.
    - Ingests a sample document.
    """
    # 1. Setup temporary paths
    user_id = "rag_test_user"
    docs_path = tmp_path / "documents"
    user_docs_path = docs_path / user_id
    user_docs_path.mkdir(parents=True)

    db_path = tmp_path / "db"
    db_path.mkdir()

    history_path = tmp_path / "history"
    history_path.mkdir()

    # 2. Monkeypatch settings and repository paths
    monkeypatch.setattr(app.core.config.settings, "VECTOR_DB_PATH", str(db_path))

    # --- DocumentRepository Patch ---
    original_doc_repo_init = app.repositories.document_repository.DocumentRepository.__init__
    def new_doc_repo_init(self, base_path=str(docs_path)):
        original_doc_repo_init(self, base_path=base_path)
    monkeypatch.setattr(app.repositories.document_repository.DocumentRepository, "__init__", new_doc_repo_init)

    # --- HistoryRepository Patch ---
    original_hist_repo_init = app.repositories.history_repository.HistoryRepository.__init__
    def new_hist_repo_init(self, user_id, db_folder=str(history_path)):
        original_hist_repo_init(self, user_id=user_id, db_folder=db_folder)
    monkeypatch.setattr(app.repositories.history_repository.HistoryRepository, "__init__", new_hist_repo_init)

    # 3. Ingest a sample document
    sample_file = user_docs_path / "sky_color.txt"
    sample_file.write_text("The sky is blue during the day.")

    # Patch the factory to inject the temporary path into the service
    original_ingestion_factory = AppFactory.create_ingestion_service
    def new_ingestion_factory(user_id):  # Correctly accept the argument
        # Re-create dependencies with patched paths for the service
        user_repo = AppFactory.create_user_repository()
        user = user_repo.get_by_id(user_id)
        return app.services.ingestion_service.IngestionService(
            user=user,
            chroma_repo=AppFactory.create_chroma_repository(),
            doc_factory=AppFactory.create_document_factory(),
            embeddings_service=AppFactory.create_embeddings_service(),
            base_doc_path=str(docs_path),
        )
    monkeypatch.setattr(AppFactory, "create_ingestion_service", new_ingestion_factory)

    ingestion_service = AppFactory.create_ingestion_service(user_id=user_id)
    ingestion_service.run_ingestion()

    return user_id


def test_full_rag_pipeline_with_context(setup_rag_environment):
    """
    Tests the full RAG pipeline:
    - A question is asked that can be answered by the ingested document.
    - The LLMService is mocked to see what context it receives.
    - Verifies that the retrieved document content is included in the prompt.
    """
    user_id = setup_rag_environment

    # Mock the final call to the LLM
    with patch("app.services.llm_service.LLMService.get_completion") as mock_get_completion:
        mock_get_completion.return_value = "The final mocked answer."

        # Get the user and the graph
        user_repo = AppFactory.create_user_repository()
        user = user_repo.get_by_id(user_id)
        app_runnable = AppFactory.create_conversation_graph()

        # Ask a question related to the ingested document
        question = "What color is the sky?"
        inputs = {"question": question, "history": [], "source_name": "sky_color.txt"}
        
        result = app_runnable.invoke(inputs)

        # 1. Assert that the final answer is the one from our mock
        assert result["answer"] == "The final mocked answer."

        # 2. The most important assertion: check if the context was in the prompt
        called_messages = mock_get_completion.call_args[0][0]
        final_prompt = called_messages[-1]["content"]

        assert "Context:" in final_prompt
        assert "The sky is blue during the day." in final_prompt
        assert "Question:" in final_prompt
        assert "What color is the sky?" in final_prompt

def test_rag_pipeline_uses_conversation_history(setup_rag_environment):
    """
    Tests that the RAG pipeline correctly uses the conversation history.
    1. A first interaction is performed to populate the history.
    2. A second, related question is asked.
    3. The LLMService is mocked to verify that the prompt for the second question
       contains the messages from the first interaction.
    """
    user_id = setup_rag_environment

    user_repo = AppFactory.create_user_repository()
    user = user_repo.get_by_id(user_id)
    app_runnable = AppFactory.create_conversation_graph()

    # 1. First interaction
    with patch("app.services.llm_service.LLMService.get_completion") as mock_get_completion_1:
        mock_get_completion_1.return_value = "It is blue."
        
        first_question = "What color is the sky?"
        inputs1 = {"question": first_question, "history": user.get_history(), "source_name": "sky_color.txt"}
        app_runnable.invoke(inputs1)
        user.add_interaction(user_message=first_question, bot_response="It is blue.")

    # 2. Second interaction
    with patch("app.services.llm_service.LLMService.get_completion") as mock_get_completion_2:
        mock_get_completion_2.return_value = "A follow-up answer."

        second_question = "Why?"
        inputs2 = {"question": second_question, "history": user.get_history(), "source_name": "sky_color.txt"}
        app_runnable.invoke(inputs2)

        # 3. Assert that the history was included in the prompt for the second call
        called_messages = mock_get_completion_2.call_args[0][0]
        
        # The full prompt should be [user_msg_1, assistant_msg_1, user_msg_2_with_context]
        assert len(called_messages) == 3
        
        # Check history
        assert called_messages[0]["role"] == "user"
        assert called_messages[0]["content"] == "What color is the sky?"
        assert called_messages[1]["role"] == "assistant"
        assert called_messages[1]["content"] == "It is blue."
        
        # Check final prompt
        final_prompt = called_messages[2]["content"]
        assert "Context:" in final_prompt
        assert "The sky is blue during the day." in final_prompt
        assert "Question:" in final_prompt
        assert "Why?" in final_prompt