"""
Course service layer for business logic
"""
from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from app.models.course import Course
from app.models.department import Department
from app.schemas.course import CourseCreate, CourseUpdate


def get_all_courses(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    dept_code: str | None = None,
    dept_id: int | None = None,
    semester: str | None = None,
    search: str | None = None,
    sort_by: str = "name",
    sort_order: str = "asc"
) -> tuple[list[Course], int]:
    """
    Get all courses with pagination, filtering, sorting, and search.
    
    Returns:
        tuple: (list of courses, total count)
    """
    query = db.query(Course)
    
    # Apply filters
    if dept_code:
        query = query.join(Department).filter(func.upper(Department.code) == dept_code.upper())
    elif dept_id:
        query = query.filter(Course.department_id == dept_id)
    
    if semester:
        query = query.filter(Course.semester == semester)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                Course.code.ilike(search_pattern),
                Course.name.ilike(search_pattern)
            )
        )
    
    # Get total count before pagination
    total = query.count()
    
    # Apply sorting
    sort_column = None
    if sort_by == "name":
        sort_column = Course.name
    elif sort_by == "code":
        sort_column = Course.code
    elif sort_by == "credits":
        sort_column = Course.credits
    elif sort_by == "semester":
        sort_column = Course.semester
    else:
        sort_column = Course.name  # Default
    
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())
    
    # Apply pagination
    offset = (page - 1) * page_size
    courses = query.offset(offset).limit(page_size).all()
    
    return courses, total


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

