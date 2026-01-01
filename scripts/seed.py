"""
Database seed script
Loads departments and courses from JSON files
"""
import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Department, Course


def seed_departments(db: Session, data: list[dict]) -> int:
    """Seed departments from JSON data. Returns count of inserted records."""
    count = 0
    for dept_data in data:
        # Check if department already exists
        existing = db.query(Department).filter(Department.code == dept_data["code"]).first()
        if existing:
            print(f"  Skipping department {dept_data['code']} (already exists)")
            continue
        
        dept = Department(code=dept_data["code"], name=dept_data["name"])
        db.add(dept)
        count += 1
    
    db.commit()
    return count


def seed_courses(db: Session, data: list[dict]) -> int:
    """Seed courses from JSON data. Returns count of inserted records."""
    count = 0
    seen_codes = set()
    
    for course_data in data:
        code = course_data["code"]
        
        # Skip duplicates in the JSON file itself
        if code in seen_codes:
            continue
        seen_codes.add(code)
        
        # Check if course already exists in DB
        existing = db.query(Course).filter(Course.code == code).first()
        if existing:
            print(f"  Skipping course {code} (already exists)")
            continue
        
        # Validate department exists
        dept = db.query(Department).filter(Department.id == course_data["department_id"]).first()
        if not dept:
            print(f"  Skipping course {code} (department_id {course_data['department_id']} not found)")
            continue
        
        course = Course(
            code=code,
            name=course_data["name"],
            credits=course_data["credits"],
            department_id=course_data["department_id"],
            max_students=course_data["max_students"],
            semester=course_data["semester"],
        )
        db.add(course)
        count += 1
    
    db.commit()
    return count


def main():
    """Main seed function."""
    base_path = Path(__file__).parent.parent
    
    print("Starting database seed...")
    
    # Load JSON files
    with open(base_path / "seed_departments.json", "r", encoding="utf-8") as f:
        departments_data = json.load(f)
    
    with open(base_path / "seed_courses.json", "r", encoding="utf-8") as f:
        courses_data = json.load(f)
    
    db = SessionLocal()
    
    try:
        print(f"\nSeeding {len(departments_data)} departments...")
        dept_count = seed_departments(db, departments_data)
        print(f"  Inserted {dept_count} departments")
        
        print(f"\nSeeding courses (from {len(courses_data)} entries, may contain duplicates)...")
        course_count = seed_courses(db, courses_data)
        print(f"  Inserted {course_count} courses")
        
        print("\nSeed completed successfully!")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

