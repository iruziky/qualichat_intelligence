# -*- coding: utf-8 -*-
"""Configuration settings for the application."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    OPENAI_API_KEY: str
    DEFAULT_MODEL: str = "gpt-4"
    VECTOR_DB_PATH: str = "./chroma_db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()

