"""
Student service layer for business logic
"""
from sqlalchemy.orm import Session

from app.models.student import Student
from app.schemas.student import StudentCreate


def get_all_students(db: Session) -> list[Student]:
    """Get all students."""
    return db.query(Student).all()


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

