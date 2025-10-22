# -*- coding: utf-8 -*-
"""Interactive terminal for testing the Qualichat Intelligence pipeline."""

# Patch for ChromaDB compatibility
__import__("pysqlite3")
import sys

sys.modules["sqlite3"] = sys.modules.pop("pysqlite3")

from app.graphs.conversation_graph import ConversationGraph
from app.core.logger import logger


def main():
    """Starts an interactive session to chat with the agent."""
    logger.info("Initializing conversation graph...")
    try:
        graph = ConversationGraph()
        graph.build()
        app_runnable = graph.compile()
        logger.info("Graph initialized. Ready for questions.")
        print("\n--- Qualichat Interactive Terminal ---")
        print("Type your question and press Enter. Type 'exit' or 'quit' to end.")

        while True:
            question = input("\n> ")
            if question.lower() in ["exit", "quit"]:
                print("Exiting...")
                break

            inputs = {"question": question}
            print("Thinking...")
            result = app_runnable.invoke(inputs)
            print("\nAssistant:")
            print(result.get("answer", "No answer found."))

    except Exception as e:
        logger.error(f"An error occurred during initialization or conversation: {e}")
        print(f"\nAn error occurred: {e}")
        print("Please check your .env file and ensure all configurations are correct.")


if __name__ == "__main__":
    main()
