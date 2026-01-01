"""
API routers
"""
from app.routers.departments import router as departments_router
from app.routers.courses import router as courses_router

__all__ = ["departments_router", "courses_router"]
