"""
SQLAlchemy models

All models are imported here for Alembic auto-detection.
"""
from app.models.department import Department
from app.models.course import Course
from app.models.student import Student
from app.models.enrollment import Enrollment
from app.models.user import User, UserRole
from app.models.prerequisite import Prerequisite

__all__ = ["Department", "Course", "Student", "Enrollment", "User", "UserRole", "Prerequisite"]
