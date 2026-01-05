"""
Student model
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Student(Base):
    """Student model representing enrolled students."""
    
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, index=True)
    student_number = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=False)
    
    # Relationships
    department = relationship("Department", back_populates="students")
    enrollments = relationship("Enrollment", back_populates="student")
    user = relationship("User", back_populates="student", uselist=False)

