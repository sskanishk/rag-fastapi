# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = "RAG FastAPI"
    DEBUG: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings object
settings = Settings()
