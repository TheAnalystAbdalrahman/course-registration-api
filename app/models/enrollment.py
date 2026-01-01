"""
Enrollment model
"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Enrollment(Base):
    """
    Enrollment model representing student-course enrollments.
    
    Uses soft delete pattern:
    - On drop: status changes to "dropped"
    - On re-enroll: same row is reactivated (status -> "enrolled", enrolled_at updated)
    
    UniqueConstraint ensures one enrollment record per student-course pair.
    """
    
    __tablename__ = "enrollments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    enrolled_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20), default="enrolled")  # enrolled/dropped
    
    # Relationships
    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")
    
    # Unique constraint: one enrollment record per student-course pair
    __table_args__ = (
        UniqueConstraint("student_id", "course_id", name="uq_student_course"),
    )

