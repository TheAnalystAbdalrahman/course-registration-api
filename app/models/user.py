"""
User model for authentication and authorization
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
import enum

from app.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    FACULTY = "faculty"
    STUDENT = "student"


class User(Base):
    """User model for authentication and role-based access control."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False, index=True)  # Stored as string, use UserRole enum for validation
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="user", uselist=False)
    
    @property
    def role_enum(self) -> UserRole:
        """Get role as UserRole enum."""
        return UserRole(self.role)
