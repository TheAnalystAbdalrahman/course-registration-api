"""
Department Pydantic schemas
"""
from pydantic import BaseModel, Field, ConfigDict


class DepartmentBase(BaseModel):
    """Base schema for Department."""
    
    code: str = Field(..., min_length=2, max_length=10, pattern=r"^[A-Z]+$")
    name: str = Field(..., min_length=3, max_length=100)


class DepartmentCreate(DepartmentBase):
    """Schema for creating a new department."""
    
    pass


class DepartmentResponse(DepartmentBase):
    """Schema for department response."""
    
    id: int
    
    model_config = ConfigDict(from_attributes=True)

