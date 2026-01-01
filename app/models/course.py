"""
Course model
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Course(Base):
    """Course model representing academic courses."""
    
    __tablename__ = "courses"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=False, nullable=False, index=True)
    name = Column(String(200), nullable=False)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    max_students = Column(Integer, nullable=False, default=30)
    semester = Column(String(20), nullable=False)
    
    # Relationships
    department = relationship("Department", back_populates="courses")
    enrollments = relationship("Enrollment", back_populates="course")

