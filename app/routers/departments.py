"""
Department API routes
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.department import DepartmentCreate, DepartmentResponse
from app.services import department_service
from app.exceptions import conflict
from app.middleware.auth import get_current_active_user, require_role
from app.models.user import User, UserRole

router = APIRouter(prefix="/api/departments", tags=["departments"])


@router.get("/", response_model=list[DepartmentResponse])
def list_departments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all departments (all authenticated users)."""
    return department_service.get_all_departments(db)


@router.post("/", response_model=DepartmentResponse, status_code=201)
def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role(UserRole.ADMIN))
):
    """Create a new department (Admin only)."""
    # Check for duplicate code
    existing = department_service.get_department_by_code(db, department.code)
    if existing:
        raise conflict(f"Department with code '{department.code}' already exists")
    return department_service.create_department(db, department)

