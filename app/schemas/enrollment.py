"""
Enrollment Pydantic schemas
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EnrollmentCreate(BaseModel):
    """Schema for creating a new enrollment."""
    
    student_id: int
    course_id: int


class EnrollmentResponse(BaseModel):
    """Schema for enrollment response."""
    
    id: int
    student_id: int
    course_id: int
    enrolled_at: datetime
    status: str
    
    model_config = ConfigDict(from_attributes=True)


class AvailabilityResponse(BaseModel):
    """Schema for course availability response."""
    
    course_id: int
    course_code: str
    max_students: int
    enrolled_count: int
    available_seats: int

