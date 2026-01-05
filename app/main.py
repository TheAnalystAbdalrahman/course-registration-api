"""
Course Registration API - Main Application Entry Point
"""
from fastapi import FastAPI

app = FastAPI(
    title="Course Registration API",
    description="API for managing course registrations, departments, students, and enrollments",
    version="1.0.0",
)


# Health check endpoint - must be registered first and work without database
@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint - always returns 200, no database dependency."""
    return {"status": "healthy"}


@app.get("/", tags=["root"])
def root():
    """Root endpoint returning API information."""
    return {
        "name": "Course Registration API",
        "version": "1.0.0",
        "docs": "/docs",
    }


# Import and register routers - these may fail if database is not configured
# but the health endpoint above will still work
try:
    from app.routers import (
        departments_router,
        courses_router,
        students_router,
        enrollments_router,
        auth_router,
        prerequisites_router
    )
    
    app.include_router(auth_router)
    app.include_router(departments_router)
    app.include_router(courses_router)
    app.include_router(students_router)
    app.include_router(enrollments_router)
    app.include_router(prerequisites_router)
except Exception as e:
    # Log the error but don't crash - health endpoint will still work
    import sys
    print(f"WARNING: Failed to register some routers: {e}", file=sys.stderr)
    print("Health endpoint is still available at /health", file=sys.stderr)

