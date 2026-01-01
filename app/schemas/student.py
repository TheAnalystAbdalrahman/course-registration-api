"""
Student Pydantic schemas
"""
from pydantic import BaseModel, Field, ConfigDict, EmailStr


class StudentBase(BaseModel):
    """Base schema for Student."""
    
    student_number: str = Field(..., min_length=5, max_length=20)
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    department_id: int


class StudentCreate(StudentBase):
    """Schema for creating a new student."""
    
    pass


class StudentResponse(StudentBase):
    """Schema for student response."""
    
    id: int
    
    model_config = ConfigDict(from_attributes=True)

