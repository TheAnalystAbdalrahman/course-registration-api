"""add prerequisites table

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-01-15 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3d4e5f6a7b8'
down_revision: Union[str, Sequence[str], None] = 'b2c3d4e5f6a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('course_prerequisites',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('prerequisite_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['prerequisite_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('course_id', 'prerequisite_id', name='uq_course_prerequisite')
    )
    op.create_index(op.f('ix_course_prerequisites_id'), 'course_prerequisites', ['id'], unique=False)
    op.create_index(op.f('ix_course_prerequisites_course_id'), 'course_prerequisites', ['course_id'], unique=False)
    op.create_index(op.f('ix_course_prerequisites_prerequisite_id'), 'course_prerequisites', ['prerequisite_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_course_prerequisites_prerequisite_id'), table_name='course_prerequisites')
    op.drop_index(op.f('ix_course_prerequisites_course_id'), table_name='course_prerequisites')
    op.drop_index(op.f('ix_course_prerequisites_id'), table_name='course_prerequisites')
    op.drop_table('course_prerequisites')
