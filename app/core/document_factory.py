# -*- coding: utf-8 -*-
"""Factory for creating Document objects from various file types."""
import uuid
from pathlib import Path
from typing import List, Dict, Callable

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    CSVLoader,
)
from langchain.text_splitter import RecursiveCharacterTextSplitter
from app.models.document import Document
from app.core.logger import logger


class DocumentFactory:
    """
    Creates a list of Document objects from a given file path.
    Supports multiple file types and performs adaptive chunking.
    """

    def __init__(self, chunk_size: int, chunk_overlap: int):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        self._loaders: Dict[str, Callable] = {
            ".txt": TextLoader,
            ".md": TextLoader,
            ".pdf": PyPDFLoader,
            ".csv": CSVLoader,
            ".yaml": TextLoader,  # Treat YAML as plain text for simplicity
            ".yml": TextLoader,
        }

    def create_documents(self, file_path: str) -> List[Document]:
        """
        Loads a file, splits it into chunks, and creates Document objects.

        Args:
            file_path: The path to the file.

        Returns:
            A list of Document objects, each representing a chunk.
        """
        path = Path(file_path)
        if not path.exists():
            logger.error(f"File not found: {file_path}")
            return []

        loader_class = self._loaders.get(path.suffix.lower())
        if not loader_class:
            logger.warning(f"Unsupported file type: {path.suffix}. Skipping.")
            return []

        try:
            logger.info(f"Loading file: {file_path} with loader {loader_class.__name__}")
            loader = loader_class(file_path)
            langchain_docs = loader.load()

            logger.info("Splitting document into chunks...")
            chunks = self.text_splitter.split_documents(langchain_docs)
            logger.success(f"Created {len(chunks)} chunks from {path.name}")

            documents: List[Document] = []
            for i, chunk in enumerate(chunks):
                doc = Document(
                    id=str(uuid.uuid4()),
                    content=chunk.page_content,
                    source_name=path.name,
                    metadata=chunk.metadata or {},
                )
                documents.append(doc)

            return documents

        except Exception as e:
            logger.error(f"Failed to process file {file_path}: {e}")
            return []
