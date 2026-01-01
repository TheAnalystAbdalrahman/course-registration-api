"""
Course API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.services import department_service, course_service
from app.exceptions import not_found, conflict, bad_request

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("/", response_model=list[CourseResponse])
def list_courses(dept: str | None = None, db: Session = Depends(get_db)):
    """Get all courses, optionally filtered by department code."""
    return course_service.get_all_courses(db, dept_code=dept)


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(course_id: int, db: Session = Depends(get_db)):
    """Get a course by ID."""
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise not_found("Course", course_id)
    return course


@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(course: CourseCreate, db: Session = Depends(get_db)):
    """Create a new course."""
    # Validate department exists
    dept = department_service.get_department_by_id(db, course.department_id)
    if not dept:
        raise bad_request(f"Department with id {course.department_id} does not exist")
    
    # Check for duplicate code
    existing = course_service.get_course_by_code(db, course.code)
    if existing:
        raise conflict(f"Course with code '{course.code}' already exists")
    
    return course_service.create_course(db, course)


@router.put("/{course_id}", response_model=CourseResponse)
def update_course(course_id: int, course: CourseUpdate, db: Session = Depends(get_db)):
    """Update an existing course."""
    updated = course_service.update_course(db, course_id, course)
    if not updated:
        raise not_found("Course", course_id)
    return updated


@router.delete("/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    """Delete a course."""
    deleted = course_service.delete_course(db, course_id)
    if not deleted:
        raise not_found("Course", course_id)

