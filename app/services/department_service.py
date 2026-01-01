"""
Department service layer for business logic
"""
from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate


def get_all_departments(db: Session) -> list[Department]:
    """Get all departments."""
    return db.query(Department).all()


def get_department_by_id(db: Session, department_id: int) -> Department | None:
    """Get a department by ID."""
    return db.query(Department).filter(Department.id == department_id).first()


def get_department_by_code(db: Session, code: str) -> Department | None:
    """Get a department by code."""
    return db.query(Department).filter(Department.code == code).first()


def create_department(db: Session, department: DepartmentCreate) -> Department:
    """Create a new department."""
    db_dept = Department(**department.model_dump())
    db.add(db_dept)
    db.commit()
    db.refresh(db_dept)
    return db_dept

