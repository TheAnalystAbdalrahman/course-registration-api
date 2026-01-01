"""
Pydantic schemas for request/response validation
"""
from app.schemas.department import DepartmentCreate, DepartmentResponse
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.schemas.student import StudentCreate, StudentResponse
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse, AvailabilityResponse

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
]
