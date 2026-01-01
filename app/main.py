"""
Course Registration API - Main Application Entry Point
"""
from fastapi import FastAPI

from app.routers import departments_router

app = FastAPI(
    title="Course Registration API",
    description="API for managing course registrations, departments, students, and enrollments",
    version="1.0.0",
)

# Register routers
app.include_router(departments_router)


@app.get("/", tags=["root"])
def root():
    """Root endpoint returning API information."""
    return {
        "name": "Course Registration API",
        "version": "1.0.0",
        "docs": "/docs",
    }


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

