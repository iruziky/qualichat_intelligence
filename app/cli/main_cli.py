# -*- coding: utf-8 -*-
"""Command-Line Interface (CLI) entry point."""
import typer
from app.graphs.conversation_graph import ConversationGraph
from app.core.logger import logger

app = typer.Typer()


@app.command()
def ask(question: str):
    """
    Ask a question to the Qualichat Intelligence.
    """
    logger.info(f"Received question: {question}")
    graph = ConversationGraph()
    graph.build()
    app_runnable = graph.compile()

    inputs = {"question": question}
    result = app_runnable.invoke(inputs)

    logger.info("Conversation finished. Final answer:")
    typer.echo(result["answer"])


if __name__ == "__main__":
    app()

