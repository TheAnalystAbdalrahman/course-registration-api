"""
Course API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.course import CourseCreate, CourseUpdate, CourseResponse
from app.schemas.student import StudentResponse
from app.schemas.enrollment import AvailabilityResponse
from app.schemas.common import PaginationParams, PaginatedResponse, CourseFilterParams, CourseSortParams
from app.services import department_service, course_service, enrollment_service
from app.exceptions import not_found, conflict, bad_request
from app.middleware.auth import get_current_active_user, require_role, require_roles
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/courses", tags=["courses"])


@router.get("/", response_model=PaginatedResponse[CourseResponse])
def list_courses(
    pagination: PaginationParams = Depends(),
    filters: CourseFilterParams = Depends(),
    sort: CourseSortParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all courses with pagination, filtering, sorting, and search (all authenticated users)."""
    courses, total = course_service.get_all_courses(
        db,
        page=pagination.page,
        page_size=pagination.page_size,
        dept_code=filters.dept_code,
        dept_id=filters.dept_id,
        semester=filters.semester,
        search=filters.search,
        sort_by=sort.sort_by,
        sort_order=sort.sort_order
    )
    return PaginatedResponse.create(
        items=courses,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size
    )


@router.get("/{course_id}", response_model=CourseResponse)
def get_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a course by ID (all authenticated users)."""
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise not_found("Course", course_id)
    return course


@router.post("/", response_model=CourseResponse, status_code=201)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.FACULTY]))
):
    """Create a new course (Admin and Faculty only)."""
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
def update_course(
    course_id: int,
    course: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.FACULTY]))
):
    """Update an existing course (Admin and Faculty only)."""
    updated = course_service.update_course(db, course_id, course)
    if not updated:
        raise not_found("Course", course_id)
    return updated


@router.delete("/{course_id}", status_code=204)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Delete a course (Admin only)."""
    deleted = course_service.delete_course(db, course_id)
    if not deleted:
        raise not_found("Course", course_id)


@router.get("/{course_id}/students", response_model=list[StudentResponse])
def get_course_students(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.FACULTY]))
):
    """Get all actively enrolled students in a course (Admin and Faculty only)."""
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise not_found("Course", course_id)
    return enrollment_service.get_students_in_course(db, course_id)


@router.get("/{course_id}/availability", response_model=AvailabilityResponse)
def get_course_availability(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get seat availability for a course (all authenticated users)."""
    availability = enrollment_service.get_course_availability(db, course_id)
    if not availability:
        raise not_found("Course", course_id)
    return availability

