"""
Application configuration using Pydantic Settings
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    database_url: str
    debug: bool = False
    
    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()

