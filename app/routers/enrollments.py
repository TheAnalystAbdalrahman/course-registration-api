"""
Enrollment API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.services import enrollment_service
from app.exceptions import not_found

router = APIRouter(prefix="/api/enrollments", tags=["enrollments"])


@router.post("/", response_model=EnrollmentResponse, status_code=201)
def create_enrollment(enrollment: EnrollmentCreate, db: Session = Depends(get_db)):
    """
    Enroll a student in a course.
    
    Business rules enforced:
    - Student must exist
    - Course must exist
    - Cannot enroll if already actively enrolled (409)
    - Cannot enroll if course is full (409)
    - Re-enrolling after dropping reactivates the existing record
    """
    return enrollment_service.create_enrollment(db, enrollment)


@router.delete("/{enrollment_id}", status_code=204)
def drop_enrollment(enrollment_id: int, db: Session = Depends(get_db)):
    """
    Drop an enrollment (soft delete).
    
    Changes status to "dropped" instead of deleting the record.
    """
    result = enrollment_service.drop_enrollment(db, enrollment_id)
    if not result:
        raise not_found("Enrollment", enrollment_id)

