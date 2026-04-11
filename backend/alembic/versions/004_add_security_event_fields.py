"""add user_agent and description to security_events

Revision ID: 004
Revises: 003
Create Date: 2026-04-10

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '004'
down_revision = '003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Add user_agent and description columns to security_events table and make user_id nullable"""
    op.add_column('security_events', sa.Column('description', sa.Text(), nullable=True))
    op.add_column('security_events', sa.Column('user_agent', sa.String(length=500), nullable=True))
    op.alter_column('security_events', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)


def downgrade() -> None:
    """Remove user_agent and description columns from security_events table and restore user_id NOT NULL"""
    op.alter_column('security_events', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.drop_column('security_events', 'user_agent')
    op.drop_column('security_events', 'description')
