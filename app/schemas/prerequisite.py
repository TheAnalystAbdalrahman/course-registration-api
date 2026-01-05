"""
Prerequisite schemas
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.course import CourseResponse


class PrerequisiteBase(BaseModel):
    """Base schema for Prerequisite."""
    
    course_id: int
    prerequisite_id: int
    
    @field_validator('prerequisite_id')
    @classmethod
    def prevent_self_reference(cls, v, info):
        """Prevent a course from being a prerequisite of itself."""
        if 'course_id' in info.data and v == info.data['course_id']:
            raise ValueError("A course cannot be a prerequisite of itself")
        return v


class PrerequisiteCreate(PrerequisiteBase):
    """Schema for creating a prerequisite relationship."""
    
    pass


class PrerequisiteResponse(PrerequisiteBase):
    """Schema for prerequisite response."""
    
    id: int
    course: Optional[CourseResponse] = None
    prerequisite: Optional[CourseResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


class PrerequisiteChain(BaseModel):
    """Schema for prerequisite chain visualization."""
    
    course_id: int
    course_code: str
    course_name: str
    direct_prerequisites: list['PrerequisiteChain']
    
    model_config = ConfigDict(from_attributes=True)


# Allow forward references for recursive structure
PrerequisiteChain.model_rebuild()
