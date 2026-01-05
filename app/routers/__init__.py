"""
API routers
"""
from app.routers.departments import router as departments_router
from app.routers.courses import router as courses_router
from app.routers.students import router as students_router
from app.routers.enrollments import router as enrollments_router
from app.routers.auth import router as auth_router
from app.routers.prerequisites import router as prerequisites_router

__all__ = [
    "departments_router",
    "courses_router",
    "students_router",
    "enrollments_router",
    "auth_router",
    "prerequisites_router"
]
