# -*- coding: utf-8 -*-
"""Interactive terminal for testing the Qualichat Intelligence pipeline."""

# Patch for ChromaDB compatibility
__import__("pypika")
__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from app.graphs.conversation_graph import ConversationGraph
from app.core.logger import logger
from app.repositories.history_repository import HistoryRepository


def main():
    """Starts an interactive session to chat with the agent."""
    logger.info("Initializing services...")
    try:
        history_repo = HistoryRepository()
        graph = ConversationGraph()
        graph.build()
        app_runnable = graph.compile()
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
            inputs = {"question": question, "history": chat_history}

            print("Thinking...")
            result = app_runnable.invoke(inputs)
            answer = result.get("answer", "No answer found.")

            # Save the new interaction to the repository
            history_repo.add_interaction(user_message=question, bot_response=answer)

            print("\nAssistant:")
            print(answer)

    except Exception as e:
        logger.error(f"An error occurred during initialization or conversation: {e}")
        print(f"\nAn error occurred: {e}")
        print("Please check your .env file and ensure all configurations are correct.")


if __name__ == "__main__":
    main()
