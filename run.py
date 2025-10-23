# -*- coding: utf-8 -*-
"""Interactive terminal for testing the Qualichat Intelligence pipeline."""

# Apply patches before any other application imports
from app.core.patches import apply_patches
apply_patches()

# --- CONFIGURATION FOR TESTING ---
# Set to a specific filename to filter RAG search, or None to search all documents.
# Example: SOURCE_DOCUMENT = "my_document.pdf"
SOURCE_DOCUMENT: str | None = "meu_documento.pdf"
USER_ID = "default_user"
# ---------------------------------

from app.core.factory import AppFactory
from app.core.logger import logger


def main():
    """Starts an interactive session to chat with the agent."""
    logger.info("Initializing services via AppFactory...")
    if SOURCE_DOCUMENT:
        logger.info(f"Target document for RAG: {SOURCE_DOCUMENT}")

    try:
        # Get the user object, which is now the main entry point for data
        user_repo = AppFactory.create_user_repository()
        user = user_repo.get_by_id(USER_ID)

        # Get the compiled graph from the factory
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
                user.clear_history()
                logger.info("Conversation history cleared.")
                print("History cleared.")
                continue

            # Get history directly from the user object
            chat_history = user.get_history()
            inputs = {
                "question": question,
                "history": chat_history,
                "source_name": SOURCE_DOCUMENT,
            }

            print("Thinking...")
            result = app_runnable.invoke(inputs)
            answer = result.get("answer", "No answer found.")

            # Save the new interaction via the user object
            user.add_interaction(user_message=question, bot_response=answer)

            print("\nAssistant:")
            print(answer)

    except Exception as e:
        logger.error(f"An error occurred during initialization or conversation: {e}", exc_info=True)
        print(f"\nAn error occurred: {e}")
        print("Please check your .env file and ensure all configurations are correct.")


if __name__ == "__main__":
    main()
