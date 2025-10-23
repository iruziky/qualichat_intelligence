# -*- coding: utf-8 -*-
"""Configuration settings for the application."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Core LLM and Vector DB settings
    OPENAI_API_KEY: str
    DEFAULT_MODEL: str = "gpt-4"
    VECTOR_DB_PATH: str = "./chroma_db"
    COLLECTION_NAME: str = "qualichat"

    # Document processing settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

