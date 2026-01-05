"""
Student service layer for business logic
"""
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate


def get_all_students(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    dept_id: int | None = None,
    search: str | None = None,
    sort_by: str = "name",
    sort_order: str = "asc"
) -> tuple[list[Student], int]:
    """
    Get all students with pagination, filtering, sorting, and search.
    
    Returns:
        tuple: (list of students, total count)
    """
    query = db.query(Student)
    
    # Apply filters
    if dept_id:
        query = query.filter(Student.department_id == dept_id)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Student.name.ilike(search_pattern),
                Student.email.ilike(search_pattern),
                Student.student_number.ilike(search_pattern)
            )
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Apply sorting
    sort_column = None
    if sort_by == "name":
        sort_column = Student.name
    elif sort_by == "email":
        sort_column = Student.email
    elif sort_by == "student_number":
        sort_column = Student.student_number
    else:
        sort_column = Student.name  # Default
    
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    students = query.offset(offset).limit(page_size).all()
    
    return students, total


def get_student_by_id(db: Session, student_id: int) -> Student | None:
    """Get a student by ID."""
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_number(db: Session, student_number: str) -> Student | None:
    """Get a student by student number."""
    return db.query(Student).filter(Student.student_number == student_number).first()


def get_student_by_email(db: Session, email: str) -> Student | None:
    """Get a student by email."""
    return db.query(Student).filter(Student.email == email).first()


def create_student(db: Session, student: StudentCreate) -> Student:
    """Create a new student."""
    db_student = Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

