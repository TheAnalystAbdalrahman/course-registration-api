"""
Pydantic schemas for request/response validation
"""
from app.schemas.department import DepartmentCreate, DepartmentResponse
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.schemas.student import StudentCreate, StudentResponse
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, AvailabilityResponse
from app.schemas.user import UserCreate, UserResponse, UserLogin, Token, TokenData
from app.schemas.common import (
    PaginationParams,
    PaginatedResponse,
    CourseFilterParams,
    CourseSortParams,
    StudentFilterParams,
    StudentSortParams
)

__all__ = [
    "DepartmentCreate",
    "DepartmentResponse",
    "CourseCreate",
    "CourseUpdate",
    "CourseResponse",
    "StudentCreate",
    "StudentResponse",
    "EnrollmentCreate",
    "EnrollmentResponse",
    "AvailabilityResponse",
    "UserCreate",
    "UserResponse",
    "UserLogin",
    "Token",
    "TokenData",
    "PaginationParams",
    "PaginatedResponse",
    "CourseFilterParams",
    "CourseSortParams",
    "StudentFilterParams",
    "StudentSortParams",
]
from app.schemas.prerequisite import (
    PrerequisiteCreate,
    PrerequisiteResponse,
    PrerequisiteChain
)

__all__.extend([
    "PrerequisiteCreate",
    "PrerequisiteResponse",
    "PrerequisiteChain",
])