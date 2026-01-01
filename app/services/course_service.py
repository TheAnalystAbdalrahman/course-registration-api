"""
Course service layer for business logic
"""
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.department import Department
from app.schemas.course import CourseCreate, CourseUpdate


def get_all_courses(db: Session, dept_code: str | None = None) -> list[Course]:
    """Get all courses, optionally filtered by department code."""
    query = db.query(Course)
    if dept_code:
        query = query.join(Department).filter(Department.code == dept_code)
    return query.all()


def get_course_by_id(db: Session, course_id: int) -> Course | None:
    """Get a course by ID."""
    return db.query(Course).filter(Course.id == course_id).first()


def get_course_by_code(db: Session, code: str) -> Course | None:
    """Get a course by code."""
    return db.query(Course).filter(Course.code == code).first()


def create_course(db: Session, course: CourseCreate) -> Course:
    """Create a new course."""
    db_course = Course(**course.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, course_update: CourseUpdate) -> Course | None:
    """Update an existing course."""
    db_course = get_course_by_id(db, course_id)
    if not db_course:
        return None
    
    # Only update fields that are provided (not None)
    update_data = course_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_course, field, value)
    
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int) -> bool:
    """Delete a course. Returns True if deleted, False if not found."""
    db_course = get_course_by_id(db, course_id)
    if not db_course:
        return False
    
    db.delete(db_course)
    db.commit()
    return True

