# -*- coding: utf-8 -*-
"""Service for intelligently ingesting documents into the vector store."""
import hashlib
import json
from pathlib import Path
from typing import Dict

from app.core.document_factory import DocumentFactory
from app.repositories.chroma_repository import ChromaRepository
from app.models.user import User
from app.services.embeddings_service import EmbeddingsService
from app.core.logger import logger


class IngestionService:
    """
    Orchestrates the ingestion of documents, processing only new or modified files.
    """

    def __init__(
        self,
        user: User,
        chroma_repo: ChromaRepository,
        doc_factory: DocumentFactory,
        embeddings_service: EmbeddingsService,
        base_doc_path: str = "documents",
    ):
        self.user = user
        self.manifest_path = Path(base_doc_path) / self.user.id / "ingestion_manifest.json"
        self.chroma_repo = chroma_repo
        self.doc_factory = doc_factory
        self.embeddings_service = embeddings_service
        self.manifest = self._load_manifest()

    def _load_manifest(self) -> Dict[str, str]:
        """Loads the ingestion manifest file, creating it if it doesn't exist."""
        if not self.manifest_path.exists():
            return {}
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

    def _save_manifest(self):
        """Saves the current state of the manifest file."""
        with open(self.manifest_path, "w", encoding="utf-8") as f:
            json.dump(self.manifest, f, indent=2)

    @staticmethod
    def _calculate_hash(file_path: Path) -> str:
        """Calculates the SHA256 hash of a file."""
        h = hashlib.sha256()
        with open(file_path, "rb") as f:
            while chunk := f.read(8192):
                h.update(chunk)
        return h.hexdigest()

    def run_ingestion(self):
        """
        Runs the full ingestion process for the user.
        It finds all documents, checks them against the manifest,
        and processes only the new or updated ones.
        """
        logger.info(f"Starting ingestion process for user: {self.user.id}")
        all_docs = self.user.get_documents()
        processed_count = 0

        for doc_path in all_docs:
            if doc_path.name == self.manifest_path.name:
                continue  # Skip the manifest file itself

            file_hash = self._calculate_hash(doc_path)
            if self.manifest.get(doc_path.name) == file_hash:
                logger.info(f"'{doc_path.name}' is unchanged. Skipping.")
                continue

            logger.warning(f"'{doc_path.name}' is new or has been modified. Processing...")

            # Process file into documents
            documents = self.doc_factory.create_documents(str(doc_path))
            if documents:
                # Generate embeddings
                contents = [doc.content for doc in documents]
                embeddings = self.embeddings_service.create_embeddings(contents)

                # Add to vector store
                self.chroma_repo.add(documents, embeddings)

                self.manifest[doc_path.name] = file_hash
                processed_count += 1
                logger.success(f"Processed and indexed '{doc_path.name}'.")

        if processed_count > 0:
            self._save_manifest()
            logger.success(
                f"Ingestion complete. Processed {processed_count} new/modified files."
            )
        else:
            logger.info("Ingestion complete. No new or modified files to process.")
