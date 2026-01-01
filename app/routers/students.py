"""
Student API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.student import StudentCreate, StudentResponse
from app.services import department_service, student_service
from app.exceptions import not_found, conflict, bad_request

router = APIRouter(prefix="/api/students", tags=["students"])


@router.get("/", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    """Get all students."""
    return student_service.get_all_students(db)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    """Get a student by ID."""
    student = student_service.get_student_by_id(db, student_id)
    if not student:
        raise not_found("Student", student_id)
    return student


@router.post("/", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    """Create a new student."""
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

