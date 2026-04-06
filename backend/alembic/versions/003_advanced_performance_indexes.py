"""Advanced performance optimization indexes and constraints

Revision ID: 003
Revises: 002
Create Date: 2024-03-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '003'
down_revision = '002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Partial indexes for better performance on filtered queries
    
    # Index only active service connections
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_service_connections_active_only
        ON service_connections (user_id, service_name, last_used_at)
        WHERE is_active = true
    """)
    
    # Index only unresolved security events
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_security_events_unresolved_only
        ON security_events (user_id, severity, timestamp)
        WHERE resolved = false
    """)
    
    # Index only pending/in-progress agent actions
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_agent_actions_active_only
        ON agent_actions (user_id, created_at, action)
        WHERE status IN ('pending', 'in_progress')
    """)
    
    # Index for recent audit logs (last 30 days optimization)
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_audit_logs_recent
        ON audit_logs (user_id, timestamp DESC, action_type)
        WHERE timestamp > (CURRENT_TIMESTAMP - INTERVAL '30 days')
    """)
    
    # Covering index for service connection lookups
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_service_connections_covering
        ON service_connections (user_id, service_name)
        INCLUDE (token_vault_id, scopes, is_active, expires_at)
    """)
    
    # GIN index for JSONB columns for better JSON queries
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_audit_logs_details_gin
        ON audit_logs USING GIN (details)
    """)
    
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_agent_actions_parameters_gin
        ON agent_actions USING GIN (parameters)
    """)
    
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_service_connections_scopes_gin
        ON service_connections USING GIN (scopes)
    """)
    
    # Hash index for exact token vault ID lookups
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_service_connections_vault_hash
        ON service_connections USING HASH (token_vault_id)
    """)
    
    # Optimize for time-based queries with BRIN indexes on timestamp columns
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_audit_logs_timestamp_brin
        ON audit_logs USING BRIN (timestamp)
    """)
    
    op.execute("""
        CREATE INDEX CONCURRENTLY ix_agent_actions_created_brin
        ON agent_actions USING BRIN (created_at)
    """)
    
    # Add table constraints for data integrity
    op.execute("""
        ALTER TABLE service_connections
        ADD CONSTRAINT chk_expires_at_future
        CHECK (expires_at IS NULL OR expires_at > created_at)
    """)
    
    op.execute("""
        ALTER TABLE agent_actions
        ADD CONSTRAINT chk_execution_time_positive
        CHECK (execution_time_ms IS NULL OR execution_time_ms >= 0)
    """)
    
    op.execute("""
        ALTER TABLE agent_actions
        ADD CONSTRAINT chk_executed_after_created
        CHECK (executed_at IS NULL OR executed_at >= created_at)
    """)


def downgrade() -> None:
    # Drop constraints
    op.execute("ALTER TABLE agent_actions DROP CONSTRAINT IF EXISTS chk_executed_after_created")
    op.execute("ALTER TABLE agent_actions DROP CONSTRAINT IF EXISTS chk_execution_time_positive")
    op.execute("ALTER TABLE service_connections DROP CONSTRAINT IF EXISTS chk_expires_at_future")
    
    # Drop indexes
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_agent_actions_created_brin")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_audit_logs_timestamp_brin")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_service_connections_vault_hash")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_service_connections_scopes_gin")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_agent_actions_parameters_gin")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_audit_logs_details_gin")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_service_connections_covering")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_audit_logs_recent")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_agent_actions_active_only")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_security_events_unresolved_only")
    op.execute("DROP INDEX CONCURRENTLY IF EXISTS ix_service_connections_active_only")