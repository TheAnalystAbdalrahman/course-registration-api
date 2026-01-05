"""
Application configuration using Pydantic Settings
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    database_url: str | None = None
    debug: bool = False
    secret_key: str = "your-secret-key-change-in-production-min-32-characters-long"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    secret_key: str = "your-secret-key-change-in-production-min-32-characters-long"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        # Try .env file if it exists, but also read from environment variables
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# Initialize settings - database_url is optional to allow app startup without DB
# Railway provides DATABASE_URL as an environment variable when database is linked
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance (for backward compatibility and explicit access)."""
    return settings

