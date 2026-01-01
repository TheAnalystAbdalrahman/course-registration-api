"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.config import get_settings

# Get settings instance
settings = get_settings()

# Create SQLAlchemy engine only if DATABASE_URL is available
# This allows the app to start even if DATABASE_URL is missing
if settings.database_url:
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    # Create a dummy engine/session for when DATABASE_URL is missing
    # This prevents crashes but database operations will fail
    engine = None
    SessionLocal = None

# Create Base class for declarative models
Base = declarative_base()


def get_db():
    """
    Dependency that provides a database session.
    Yields a session and ensures it's closed after use.
    """
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured. Cannot create database session.")
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

