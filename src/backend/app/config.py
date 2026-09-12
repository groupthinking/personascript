"""
Backend API Configuration Settings for PersonaScript.
"""

import os
from pydantic import BaseModel, Field


class Settings(BaseModel):
    """Application settings and environment parameters."""

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "PersonaScript Backend API"
    VERSION: str = "1.0.0"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "personascript-secret-key-change-in-production-123456789")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database & Cache
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://personascript:personascript_password@localhost:5432/personascript_db"
    )
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # AI API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")


settings = Settings()
