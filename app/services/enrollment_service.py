"""
Enrollment service layer for business logic

Implements critical business rules:
- Seat availability checking
- Duplicate enrollment prevention
- Soft delete (status -> "dropped")
- Re-enrollment (reactivate existing record)
"""
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.enrollment import Enrollment
from app.models.student import Student
from app.schemas.enrollment import EnrollmentCreate
from app.services import student_service, course_service
from app.exceptions import bad_request, conflict


def get_enrolled_count(db: Session, course_id: int) -> int:
    """Get count of active enrollments for a course."""
    return db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.status == "enrolled"
    ).count()


def get_enrollment_by_student_and_course(
    db: Session, student_id: int, course_id: int
) -> Enrollment | None:
    """Get enrollment record for a student-course pair (any status)."""
    return db.query(Enrollment).filter(
        Enrollment.student_id == student_id,
        Enrollment.course_id == course_id
    ).first()


def get_enrollment_by_id(db: Session, enrollment_id: int) -> Enrollment | None:
    """Get enrollment by ID."""
    return db.query(Enrollment).filter(Enrollment.id == enrollment_id).first()


def create_enrollment(db: Session, enrollment: EnrollmentCreate) -> Enrollment:
    """
    Create or reactivate an enrollment.
    
    Business rules:
    1. Student must exist
    2. Course must exist
    3. Cannot enroll if already actively enrolled
    4. Cannot enroll if course is full
    5. If previously dropped, reactivate the existing record
    """
    # Validate student exists
    student = student_service.get_student_by_id(db, enrollment.student_id)
    if not student:
        raise bad_request(f"Student with id {enrollment.student_id} does not exist")
    
    # Validate course exists
    course = course_service.get_course_by_id(db, enrollment.course_id)
    if not course:
        raise bad_request(f"Course with id {enrollment.course_id} does not exist")
    
    # Check for existing enrollment record
    existing = get_enrollment_by_student_and_course(
        db, enrollment.student_id, enrollment.course_id
    )
    
    if existing:
        if existing.status == "enrolled":
            # Already actively enrolled
            raise conflict("Student is already enrolled in this course")
        else:
            # Previously dropped - reactivate
            # First check seat availability
            enrolled_count = get_enrolled_count(db, enrollment.course_id)
            if enrolled_count >= course.max_students:
                raise conflict(f"Course is full ({course.max_students} seats)")
            
            # Reactivate the enrollment
            existing.status = "enrolled"
            existing.enrolled_at = datetime.utcnow()
            db.commit()
            db.refresh(existing)
            return existing
    
    # New enrollment - check seat availability
    enrolled_count = get_enrolled_count(db, enrollment.course_id)
    if enrolled_count >= course.max_students:
        raise conflict(f"Course is full ({course.max_students} seats)")
    
    # Create new enrollment
    db_enrollment = Enrollment(**enrollment.model_dump())
    db.add(db_enrollment)
    db.commit()
    db.refresh(db_enrollment)
    return db_enrollment


def drop_enrollment(db: Session, enrollment_id: int) -> Enrollment | None:
    """
    Drop an enrollment (soft delete - status -> "dropped").
    Returns the updated enrollment or None if not found.
    """
    enrollment = get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        return None
    
    if enrollment.status == "dropped":
        # Already dropped, just return it
        return enrollment
    
    enrollment.status = "dropped"
    db.commit()
    db.refresh(enrollment)
    return enrollment


def get_student_enrollments(db: Session, student_id: int) -> list[Enrollment]:
    """Get all enrollments for a student."""
    return db.query(Enrollment).filter(Enrollment.student_id == student_id).all()


def get_students_in_course(db: Session, course_id: int) -> list[Student]:
    """Get all actively enrolled students in a course."""
    enrollments = db.query(Enrollment).filter(
        Enrollment.course_id == course_id,
        Enrollment.status == "enrolled"
    ).all()
    return [e.student for e in enrollments]


def get_course_availability(db: Session, course_id: int) -> dict | None:
    """Get course availability information."""
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        return None
    
    enrolled_count = get_enrolled_count(db, course_id)
    return {
        "course_id": course.id,
        "course_code": course.code,
        "max_students": course.max_students,
        "enrolled_count": enrolled_count,
        "available_seats": course.max_students - enrolled_count
    }

