"""
Application configuration using Pydantic Settings
"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    database_url: str
    debug: bool = False
    
    class Config:
        # Try .env file if it exists, but also read from environment variables
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


# Initialize settings
# Railway provides DATABASE_URL as an environment variable
settings = Settings()

