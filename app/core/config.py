# app/core/config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional
import json

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
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int

    # CORS
    # CORS - load from either JSON or comma-separated string
    ALLOWED_ORIGINS_RAW: Optional[str] = None

    @property
    def ALLOWED_ORIGINS(self) -> List[str]:
        if not self.ALLOWED_ORIGINS_RAW:
            return []
        try:
            # Try JSON first
            return json.loads(self.ALLOWED_ORIGINS_RAW)
        except json.JSONDecodeError:
            # Fall back to comma-separated
            return [origin.strip() for origin in self.ALLOWED_ORIGINS_RAW.split(",")]

    # DB
    DATABASE_URL: Optional[str] = None

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
