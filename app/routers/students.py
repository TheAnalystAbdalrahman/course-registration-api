"""
Student API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.schemas.enrollment import EnrollmentResponse
from app.schemas.common import PaginationParams, PaginatedResponse, StudentFilterParams, StudentSortParams
from app.services import department_service, student_service, enrollment_service
from app.exceptions import not_found, conflict, bad_request
from app.middleware.auth import get_current_active_user, require_role, require_roles
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("/", response_model=PaginatedResponse[StudentResponse])
def list_students(
    pagination: PaginationParams = Depends(),
    filters: StudentFilterParams = Depends(),
    sort: StudentSortParams = Depends(),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.FACULTY]))
):
    """Get all students with pagination, filtering, sorting, and search (Admin and Faculty only)."""
    students, total = student_service.get_all_students(
        db,
        page=pagination.page,
        page_size=pagination.page_size,
        dept_id=filters.dept_id,
        search=filters.search,
        sort_by=sort.sort_by,
        sort_order=sort.sort_order
    )
    return PaginatedResponse.create(
        items=students,
        total=total,
        page=pagination.page,
        page_size=pagination.page_size
    )


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get a student by ID."""
    # Students can only view their own profile, Admin/Faculty can view any
    if current_user.role == UserRole.STUDENT:
        if current_user.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only view their own profile"
            )
    
    student = student_service.get_student_by_id(db, student_id)
    if not student:
        raise not_found("Student", student_id)
    return student


@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Create a new student (Admin only)."""
    # Validate department exists
    dept = department_service.get_department_by_id(db, student.department_id)
    if not dept:
        raise bad_request(f"Department with id {student.department_id} does not exist")
    
    # Check for duplicate email
    existing_email = student_service.get_student_by_email(db, student.email)
    if existing_email:
        raise conflict(f"Student with email '{student.email}' already exists")
    
    # Check for duplicate student number
    existing_number = student_service.get_student_by_number(db, student.student_number)
    if existing_number:
        raise conflict(f"Student with number '{student.student_number}' already exists")
    
    return student_service.create_student(db, student)


@router.get("/{student_id}/enrollments", response_model=list[EnrollmentResponse])
def get_student_enrollments(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all enrollments for a student."""
    # Students can only view their own enrollments, Admin/Faculty can view any
    if current_user.role == UserRole.STUDENT:
        if current_user.student_id != student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only view their own enrollments"
            )
    
    student = student_service.get_student_by_id(db, student_id)
    if not student:
        raise not_found("Student", student_id)
    return enrollment_service.get_student_enrollments(db, student_id)

