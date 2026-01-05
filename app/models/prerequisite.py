"""
Prerequisite model for course prerequisites
"""
from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Prerequisite(Base):
    """
    Prerequisite model representing course prerequisites.
    
    Many-to-many relationship between courses (self-referential).
    """
    
    __tablename__ = "course_prerequisites"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    prerequisite_id = Column(Integer, ForeignKey("courses.id"), nullable=False, index=True)
    
    # Relationships
    course = relationship("Course", foreign_keys=[course_id], back_populates="prerequisites")
    prerequisite = relationship("Course", foreign_keys=[prerequisite_id], back_populates="is_prerequisite_for")
    
    # Unique constraint: prevent duplicate prerequisite relationships
    __table_args__ = (
        UniqueConstraint("course_id", "prerequisite_id", name="uq_course_prerequisite"),
    )
