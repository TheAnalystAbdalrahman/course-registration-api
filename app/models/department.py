"""
Department model
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Department(Base):
    """Department model representing academic departments."""
    
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    
    # Relationships
    courses = relationship("Course", back_populates="department")
    students = relationship("Student", back_populates="department")

