# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyHttpUrl
from typing import List, Optional

class Settings(BaseSettings):
    # App settings
    APP_NAME: str
    APP_HOST: str
    APP_PORT: int
    DEBUG: bool

    # Security
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # CORS
    ALLOWED_ORIGINS: List[str]

    # DB
    DATABASE_URL: Optional[str]

    # LLM
    OPENAI_API_KEY: Optional[str]
    LOCAL_LLM_PATH: Optional[str]

    # Pydantic V2 Config (replaces class Config)
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",  # Recommended to avoid encoding issues
        extra="allow",  # Allows extra fields (if needed)
        case_sensitive=True,  # Makes env var names case-sensitive
    )

# Singleton instance to use across application
settings = Settings()
