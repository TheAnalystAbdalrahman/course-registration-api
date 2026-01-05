"""
Common schemas for pagination, filtering, and sorting
"""
from typing import Generic, TypeVar, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')


class PaginationParams(BaseModel):
    """Pagination parameters."""
    
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    page_size: int = Field(default=20, ge=1, le=100, description="Number of items per page")


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper."""
    
    items: list[T]
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    page_size: int = Field(description="Number of items per page")
    total_pages: int = Field(description="Total number of pages")
    
    @classmethod
    def create(cls, items: list[T], total: int, page: int, page_size: int):
        """Create a paginated response."""
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )


class CourseFilterParams(BaseModel):
    """Filter parameters for courses."""
    
    dept_code: Optional[str] = Field(default=None, description="Filter by department code")
    dept_id: Optional[int] = Field(default=None, description="Filter by department ID")
    semester: Optional[str] = Field(default=None, description="Filter by semester (e.g., 'Fall 2024')")
    search: Optional[str] = Field(default=None, description="Search in course code and name")


class CourseSortParams(BaseModel):
    """Sort parameters for courses."""
    
    sort_by: str = Field(default="name", description="Field to sort by (name, code, credits, semester)")
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)")


class StudentFilterParams(BaseModel):
    """Filter parameters for students."""
    
    dept_id: Optional[int] = Field(default=None, description="Filter by department ID")
    search: Optional[str] = Field(default=None, description="Search in name, email, or student number")


class StudentSortParams(BaseModel):
    """Sort parameters for students."""
    
    sort_by: str = Field(default="name", description="Field to sort by (name, email, student_number)")
    sort_order: str = Field(default="asc", pattern="^(asc|desc)$", description="Sort order (asc or desc)")
