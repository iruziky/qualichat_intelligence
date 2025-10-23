# -*- coding: utf-8 -*-
"""Interactive terminal for testing the Qualichat Intelligence pipeline."""

# Patch for ChromaDB compatibility
__import__("pypika")
__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

# --- CONFIGURATION FOR TESTING ---
# Set to a specific filename to filter RAG search, or None to search all documents.
# Example: SOURCE_DOCUMENT = "my_document.pdf"
SOURCE_DOCUMENT: str | None = "meu_documento.pdf"
# ---------------------------------

from app.core.factory import AppFactory
from app.core.logger import logger
from app.models.history import HistoryItem


def main():
    """Starts an interactive session to chat with the agent."""
    logger.info("Initializing services via AppFactory...")
    if SOURCE_DOCUMENT:
        logger.info(f"Target document for RAG: {SOURCE_DOCUMENT}")

    try:
        # Use the factory to get components
        history_repo = AppFactory.create_history_repository()
        app_runnable = AppFactory.create_conversation_graph()
        
        logger.info("Initialization complete. Ready for questions.")
        print("\n--- Qualichat Interactive Terminal ---")
        print("Type your question and press Enter. Type 'exit', 'quit', or 'clear'.")

        while True:
            question = input("\n> ")
            if question.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            if question.lower() == "clear":
                history_repo.clear_history()
                logger.info("Conversation history cleared.")
                print("History cleared.")
                continue

            # Get history from the repository
            chat_history = history_repo.get_history()
            inputs = {
                "question": question,
                "history": chat_history,
                "source_name": SOURCE_DOCUMENT,
            }

            print("Thinking...")
            result = app_runnable.invoke(inputs)
            answer = result.get("answer", "No answer found.")

            # Save the new interaction to the repository
            history_item = HistoryItem(user_message=question, bot_response=answer)
            history_repo.add_interaction(history_item)

            print("\nAssistant:")
            print(answer)

    except Exception as e:
        logger.error(f"An error occurred during initialization or conversation: {e}")
        print(f"\nAn error occurred: {e}")
        print("Please check your .env file and ensure all configurations are correct.")


if __name__ == "__main__":
    main()
