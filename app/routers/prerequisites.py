"""
Prerequisite API routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.prerequisite import PrerequisiteCreate, PrerequisiteResponse, PrerequisiteChain
from app.services import prerequisite_service, course_service
from app.exceptions import not_found
from app.middleware.auth import get_current_active_user, require_roles
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/courses", tags=["prerequisites"])


@router.post("/{course_id}/prerequisites", response_model=PrerequisiteResponse, status_code=201)
def add_prerequisite(
    course_id: int,
    prerequisite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.FACULTY]))
):
    """Add a prerequisite to a course (Admin and Faculty only)."""
    # Validate course exists
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise not_found("Course", course_id)
    
    prerequisite = PrerequisiteCreate(course_id=course_id, prerequisite_id=prerequisite_id)
    return prerequisite_service.add_prerequisite(db, prerequisite)


@router.delete("/{course_id}/prerequisites/{prerequisite_id}", status_code=204)
def remove_prerequisite(
    course_id: int,
    prerequisite_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles([UserRole.ADMIN, UserRole.FACULTY]))
):
    """Remove a prerequisite from a course (Admin and Faculty only)."""
    # Validate course exists
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise not_found("Course", course_id)
    
    result = prerequisite_service.remove_prerequisite(db, course_id, prerequisite_id)
    if not result:
        raise not_found("Prerequisite", prerequisite_id)


@router.get("/{course_id}/prerequisites", response_model=list[PrerequisiteResponse])
def get_prerequisites(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all direct prerequisites for a course (all authenticated users)."""
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise not_found("Course", course_id)
    
    direct_prereqs = prerequisite_service.get_direct_prerequisites(db, course_id)
    # Convert to PrerequisiteResponse format
    prerequisites = []
    for prereq in direct_prereqs:
        prereq_rel = prerequisite_service.get_prerequisite_by_course_and_prerequisite(
            db, course_id, prereq.id
        )
        if prereq_rel:
            prerequisites.append(prereq_rel)
    
    return prerequisites


@router.get("/{course_id}/prerequisites/chain", response_model=PrerequisiteChain)
def get_prerequisite_chain(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get full prerequisite chain for a course (all authenticated users)."""
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise not_found("Course", course_id)
    
    chain = prerequisite_service.get_prerequisite_chain(db, course_id)
    if not chain:
        raise not_found("Course", course_id)
    
    return chain


@router.get("/{course_id}/prerequisites/check/{student_id}")
def check_prerequisites(
    course_id: int,
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Check if a student meets all prerequisites for a course (all authenticated users)."""
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        raise not_found("Course", course_id)
    
    from app.services import student_service
    student = student_service.get_student_by_id(db, student_id)
    if not student:
        raise not_found("Student", student_id)
    
    all_met, missing = prerequisite_service.check_prerequisites_met(db, student_id, course_id)
    
    return {
        "course_id": course_id,
        "student_id": student_id,
        "all_prerequisites_met": all_met,
        "missing_prerequisites": [
            {"id": p.id, "code": p.code, "name": p.name} for p in missing
        ]
    }
