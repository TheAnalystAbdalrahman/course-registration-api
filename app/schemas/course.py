"""
Course Pydantic schemas
"""
from pydantic import BaseModel, Field, ConfigDict


class CourseBase(BaseModel):
    """Base schema for Course."""
    
    code: str = Field(..., min_length=3, max_length=20)
    name: str = Field(..., min_length=3, max_length=200)
    credits: int = Field(..., ge=1, le=6)
    department_id: int
    max_students: int = Field(default=30, ge=1, le=500)
    semester: str = Field(..., pattern=r"^(Fall|Spring|Summer) \d{4}$")


class CourseCreate(CourseBase):
    """Schema for creating a new course."""
    
    pass


class CourseUpdate(BaseModel):
    """Schema for updating a course (partial update)."""
    
    name: str | None = Field(default=None, min_length=3, max_length=200)
    credits: int | None = Field(default=None, ge=1, le=6)
    max_students: int | None = Field(default=None, ge=1, le=500)
    semester: str | None = Field(default=None, pattern=r"^(Fall|Spring|Summer) \d{4}$")


class CourseResponse(CourseBase):
    """Schema for course response."""
    
    id: int
    
    model_config = ConfigDict(from_attributes=True)

