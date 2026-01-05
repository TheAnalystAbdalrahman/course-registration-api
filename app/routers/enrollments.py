"""
Enrollment API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.enrollment import EnrollmentCreate, EnrollmentResponse
from app.services import enrollment_service
from app.exceptions import not_found
from app.middleware.auth import get_current_active_user, require_role, require_roles
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/enrollments", tags=["enrollments"])


@router.post("/", response_model=EnrollmentResponse, status_code=201)
def create_enrollment(
    enrollment: EnrollmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Enroll a student in a course.
    
    Students can only enroll themselves. Admin/Faculty can enroll any student.
    
    Business rules enforced:
    - Student must exist
    - Course must exist
    - Cannot enroll if already actively enrolled (409)
    - Cannot enroll if course is full (409)
    - Re-enrolling after dropping reactivates the existing record
    """
    # Students can only enroll themselves
    if current_user.role == UserRole.STUDENT:
        if current_user.student_id != enrollment.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only enroll themselves"
            )
    
    return enrollment_service.create_enrollment(db, enrollment)


@router.delete("/{enrollment_id}", status_code=204)
def drop_enrollment(
    enrollment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Drop an enrollment (soft delete).
    
    Students can only drop their own enrollments. Admin/Faculty can drop any enrollment.
    
    Changes status to "dropped" instead of deleting the record.
    """
    # Get enrollment to check ownership
    enrollment = enrollment_service.get_enrollment_by_id(db, enrollment_id)
    if not enrollment:
        raise not_found("Enrollment", enrollment_id)
    
    # Students can only drop their own enrollments
    if current_user.role == UserRole.STUDENT:
        if current_user.student_id != enrollment.student_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Students can only drop their own enrollments"
            )
    
    result = enrollment_service.drop_enrollment(db, enrollment_id)
    if not result:
        raise not_found("Enrollment", enrollment_id)

