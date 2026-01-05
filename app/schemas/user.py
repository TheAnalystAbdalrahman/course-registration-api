"""
User authentication and authorization schemas
"""
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr, ConfigDict

from app.models.user import UserRole


class UserBase(BaseModel):
    """Base schema for User."""
    
    email: EmailStr
    role: UserRole


class UserCreate(UserBase):
    """Schema for creating a new user."""
    
    password: str = Field(..., min_length=8, max_length=100)
    student_id: int | None = None


class UserLogin(BaseModel):
    """Schema for user login."""
    
    email: EmailStr
    password: str


class UserResponse(UserBase):
    """Schema for user response (excludes password)."""
    
    id: int
    student_id: int | None = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    """Schema for JWT token response."""
    
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema for JWT token payload data."""
    
    email: str | None = None
    role: str | None = None
