"""add search indexes

Revision ID: b2c3d4e5f6a7
Revises: a1b2c3d4e5f6
Create Date: 2026-01-15 11:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6a7'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add indexes for course search and filtering
    op.create_index('ix_courses_name', 'courses', ['name'], unique=False)
    op.create_index('ix_courses_semester', 'courses', ['semester'], unique=False)
    
    # Add indexes for student search
    op.create_index('ix_students_name', 'students', ['name'], unique=False)
    op.create_index('ix_students_email', 'students', ['email'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index('ix_students_email', table_name='students')
    op.drop_index('ix_students_name', table_name='students')
    op.drop_index('ix_courses_semester', table_name='courses')
    op.drop_index('ix_courses_name', table_name='courses')
