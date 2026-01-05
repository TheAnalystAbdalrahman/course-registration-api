"""
Prerequisite service for managing course prerequisites
"""
from typing import Optional
from sqlalchemy.orm import Session

from app.models.prerequisite import Prerequisite
from app.models.course import Course
from app.schemas.prerequisite import PrerequisiteCreate
from app.services import course_service, enrollment_service
from app.exceptions import bad_request, conflict


def get_prerequisite_by_id(db: Session, prerequisite_id: int) -> Optional[Prerequisite]:
    """Get a prerequisite by ID."""
    return db.query(Prerequisite).filter(Prerequisite.id == prerequisite_id).first()


def get_prerequisite_by_course_and_prerequisite(
    db: Session, course_id: int, prerequisite_id: int
) -> Optional[Prerequisite]:
    """Get a prerequisite relationship by course and prerequisite IDs."""
    return db.query(Prerequisite).filter(
        Prerequisite.course_id == course_id,
        Prerequisite.prerequisite_id == prerequisite_id
    ).first()


def get_direct_prerequisites(db: Session, course_id: int) -> list[Course]:
    """Get direct prerequisites for a course."""
    prerequisites = db.query(Prerequisite).filter(
        Prerequisite.course_id == course_id
    ).all()
    return [p.prerequisite for p in prerequisites]


def get_all_prerequisites(db: Session, course_id: int) -> list[Course]:
    """
    Get all prerequisites recursively (direct and indirect).
    
    Uses depth-first search to traverse the prerequisite chain.
    """
    visited = set()
    result = []
    
    def dfs(course_id: int):
        if course_id in visited:
            return
        visited.add(course_id)
        
        direct_prereqs = get_direct_prerequisites(db, course_id)
        for prereq in direct_prereqs:
            if prereq.id not in visited:
                result.append(prereq)
                dfs(prereq.id)
    
    dfs(course_id)
    return result


def has_circular_dependency(db: Session, course_id: int, prerequisite_id: int) -> bool:
    """
    Check if adding a prerequisite would create a circular dependency.
    
    Uses DFS to check if prerequisite_id is reachable from course_id
    through the prerequisite chain.
    """
    visited = set()
    
    def dfs(current_id: int) -> bool:
        if current_id == course_id:
            return True  # Circular dependency found
        if current_id in visited:
            return False
        visited.add(current_id)
        
        direct_prereqs = get_direct_prerequisites(db, current_id)
        for prereq in direct_prereqs:
            if dfs(prereq.id):
                return True
        return False
    
    return dfs(prerequisite_id)


def add_prerequisite(db: Session, prerequisite: PrerequisiteCreate) -> Prerequisite:
    """
    Add a prerequisite relationship.
    
    Validates:
    - Both courses exist
    - No self-reference
    - No circular dependencies
    - No duplicate relationships
    """
    # Validate courses exist
    course = course_service.get_course_by_id(db, prerequisite.course_id)
    if not course:
        raise bad_request(f"Course with id {prerequisite.course_id} does not exist")
    
    prereq_course = course_service.get_course_by_id(db, prerequisite.prerequisite_id)
    if not prereq_course:
        raise bad_request(f"Prerequisite course with id {prerequisite.prerequisite_id} does not exist")
    
    # Prevent self-reference
    if prerequisite.course_id == prerequisite.prerequisite_id:
        raise bad_request("A course cannot be a prerequisite of itself")
    
    # Check for duplicate
    existing = get_prerequisite_by_course_and_prerequisite(
        db, prerequisite.course_id, prerequisite.prerequisite_id
    )
    if existing:
        raise conflict(
            f"Prerequisite relationship already exists between course {prerequisite.course_id} "
            f"and prerequisite {prerequisite.prerequisite_id}"
        )
    
    # Check for circular dependency
    if has_circular_dependency(db, prerequisite.course_id, prerequisite.prerequisite_id):
        raise bad_request(
            f"Adding this prerequisite would create a circular dependency"
        )
    
    # Create prerequisite
    db_prerequisite = Prerequisite(**prerequisite.model_dump())
    db.add(db_prerequisite)
    db.commit()
    db.refresh(db_prerequisite)
    return db_prerequisite


def remove_prerequisite(db: Session, course_id: int, prerequisite_id: int) -> bool:
    """Remove a prerequisite relationship."""
    prerequisite = get_prerequisite_by_course_and_prerequisite(db, course_id, prerequisite_id)
    if not prerequisite:
        return False
    
    db.delete(prerequisite)
    db.commit()
    return True


def get_prerequisite_chain(db: Session, course_id: int) -> dict:
    """
    Get full prerequisite chain as a nested structure.
    
    Returns a dictionary with course info and nested prerequisites.
    """
    course = course_service.get_course_by_id(db, course_id)
    if not course:
        return None
    
    direct_prereqs = get_direct_prerequisites(db, course_id)
    chain = {
        "course_id": course.id,
        "course_code": course.code,
        "course_name": course.name,
        "direct_prerequisites": [
            get_prerequisite_chain(db, prereq.id) for prereq in direct_prereqs
        ]
    }
    return chain


def check_prerequisites_met(
    db: Session, student_id: int, course_id: int
) -> tuple[bool, list[Course]]:
    """
    Check if a student has met all prerequisites for a course.
    
    Returns:
        tuple: (all_met: bool, missing_prerequisites: list[Course])
    """
    # Get all prerequisites (direct and indirect)
    all_prereqs = get_all_prerequisites(db, course_id)
    
    if not all_prereqs:
        return True, []  # No prerequisites
    
    # Get student's enrollments
    student_enrollments = enrollment_service.get_student_enrollments(db, student_id)
    
    # Check which prerequisites are met (student is enrolled)
    enrolled_course_ids = {
        e.course_id for e in student_enrollments if e.status == "enrolled"
    }
    
    missing = [prereq for prereq in all_prereqs if prereq.id not in enrolled_course_ids]
    
    return len(missing) == 0, missing
