"""Add performance optimization indexes

Revision ID: 002
Revises: 001
Create Date: 2024-03-26 10:30:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Composite indexes for common query patterns
    
    # User + Service combination for service connections
    op.create_index(
        'ix_service_connections_user_service',
        'service_connections',
        ['user_id', 'service_name'],
        unique=False
    )
    
    # User + Active status for active connections
    op.create_index(
        'ix_service_connections_user_active',
        'service_connections',
        ['user_id', 'is_active'],
        unique=False
    )
    
    # User + Timestamp for audit log queries
    op.create_index(
        'ix_audit_logs_user_timestamp',
        'audit_logs',
        ['user_id', 'timestamp'],
        unique=False
    )
    
    # Action type + Timestamp for audit filtering
    op.create_index(
        'ix_audit_logs_action_timestamp',
        'audit_logs',
        ['action_type', 'timestamp'],
        unique=False
    )
    
    # User + Status for agent action queries
    op.create_index(
        'ix_agent_actions_user_status',
        'agent_actions',
        ['user_id', 'status'],
        unique=False
    )
    
    # User + Created timestamp for chronological queries
    op.create_index(
        'ix_agent_actions_user_created',
        'agent_actions',
        ['user_id', 'created_at'],
        unique=False
    )
    
    # Service + Scope for permission template lookups
    op.create_index(
        'ix_permission_templates_service_scope',
        'permission_templates',
        ['service_name', 'scope_name'],
        unique=True  # Ensure unique service-scope combinations
    )
    
    # Risk level + Step-up requirement for security queries
    op.create_index(
        'ix_permission_templates_risk_stepup',
        'permission_templates',
        ['risk_level', 'requires_step_up'],
        unique=False
    )
    
    # User + Severity for security event queries
    op.create_index(
        'ix_security_events_user_severity',
        'security_events',
        ['user_id', 'severity'],
        unique=False
    )
    
    # Unresolved events for monitoring
    op.create_index(
        'ix_security_events_unresolved',
        'security_events',
        ['resolved', 'severity', 'timestamp'],
        unique=False
    )
    
    # Token Vault ID for quick lookups
    op.create_index(
        'ix_service_connections_vault_lookup',
        'service_connections',
        ['token_vault_id', 'is_active'],
        unique=False
    )


def downgrade() -> None:
    # Drop composite indexes
    op.drop_index('ix_service_connections_vault_lookup', table_name='service_connections')
    op.drop_index('ix_security_events_unresolved', table_name='security_events')
    op.drop_index('ix_security_events_user_severity', table_name='security_events')
    op.drop_index('ix_permission_templates_risk_stepup', table_name='permission_templates')
    op.drop_index('ix_permission_templates_service_scope', table_name='permission_templates')
    op.drop_index('ix_agent_actions_user_created', table_name='agent_actions')
    op.drop_index('ix_agent_actions_user_status', table_name='agent_actions')
    op.drop_index('ix_audit_logs_action_timestamp', table_name='audit_logs')
    op.drop_index('ix_audit_logs_user_timestamp', table_name='audit_logs')
    op.drop_index('ix_service_connections_user_active', table_name='service_connections')
    op.drop_index('ix_service_connections_user_service', table_name='service_connections')