# CipherMate Database Setup

This document describes the database setup and management for the CipherMate platform.

## Database Schema

The CipherMate platform uses PostgreSQL with the following core tables:

### Core Tables

1. **users** - User account information
   - Stores Auth0 user IDs and basic profile data
   - Links to all user-related activities

2. **service_connections** - Third-party service integrations
   - Tracks connections to Google, GitHub, Slack, etc.
   - References Auth0 Token Vault for secure token storage
   - Manages permission scopes and expiration

3. **audit_logs** - Comprehensive activity logging
   - Records all user actions and system events
   - Includes IP addresses, user agents, and session tracking
   - Supports compliance and security monitoring

4. **agent_actions** - AI agent operation tracking
   - Logs all actions performed by AI agents
   - Tracks execution status and performance metrics
   - Supports step-up authentication requirements

5. **permission_templates** - Service permission definitions
   - Defines available permissions for each service
   - Categorizes risk levels and step-up requirements
   - Supports dynamic permission management

6. **security_events** - Security incident tracking
   - Monitors authentication failures and suspicious activities
   - Supports incident response and threat detection
   - Tracks resolution status

## Database Management

### Setup Commands

```bash
# Initialize database (create tables)
python manage_db.py init

# Run Alembic migrations
python manage_db.py migrate

# Seed with initial data (permission templates)
python manage_db.py seed

# Create sample data for development
python manage_db.py sample

# Reset database (WARNING: deletes all data)
python manage_db.py reset
```

### Development Workflow

1. **Initial Setup**:
   ```bash
   python manage_db.py migrate
   python manage_db.py seed
   ```

2. **Adding Sample Data**:
   ```bash
   python manage_db.py sample
   ```

3. **Testing Models**:
   ```bash
   python test_models.py
   ```

### Migration Management

Migrations are managed using Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migrations
alembic downgrade -1
```

## Performance Optimizations

### Indexes

The database includes optimized indexes for common query patterns:

- **Composite Indexes**: User + Service, User + Timestamp combinations
- **Lookup Indexes**: Token Vault ID, Auth0 ID, Session ID
- **Filtering Indexes**: Status, Active flags, Risk levels
- **Unique Constraints**: Service-scope combinations, Auth0 IDs

### Query Optimization

- Use the utility functions in `app/db/utils.py` for common operations
- Leverage SQLAlchemy's `selectinload()` for relationship loading
- Implement proper pagination for large result sets
- Use database-level filtering instead of application-level filtering

## Security Considerations

### Data Protection

- **Sensitive Data**: Never store actual tokens in the database
- **Token References**: Only store Token Vault IDs from Auth0
- **Audit Trails**: Comprehensive logging without exposing sensitive information
- **Data Retention**: Implement appropriate retention policies for audit data

### Access Control

- **Database Users**: Use separate database users for different environments
- **Connection Pooling**: Implement proper connection management
- **SSL/TLS**: Always use encrypted connections in production
- **Backup Security**: Encrypt database backups and restrict access

## Monitoring and Maintenance

### Health Checks

- Monitor database connection pool status
- Track query performance and slow queries
- Monitor disk usage and growth patterns
- Set up alerts for connection failures

### Maintenance Tasks

- **Regular Cleanup**: Remove expired connections and old audit logs
- **Index Maintenance**: Monitor and rebuild indexes as needed
- **Statistics Updates**: Keep database statistics current for query optimization
- **Backup Verification**: Regularly test backup and restore procedures

### Utility Functions

The `app/db/utils.py` module provides helper functions for:

- User management and lookup
- Service connection management
- Audit logging and retrieval
- Security event tracking
- Performance statistics
- Data cleanup operations

## Environment Configuration

### Development

```bash
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ciphermate_dev
```

### Production

```bash
DATABASE_URL=postgresql+asyncpg://user:password@host:5432/ciphermate_prod
```

### Docker Compose

The project includes a Docker Compose configuration for local development:

```yaml
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_DB: ciphermate
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
```

## Troubleshooting

### Common Issues

1. **Migration Failures**: Check for conflicting schema changes
2. **Connection Errors**: Verify database URL and credentials
3. **Performance Issues**: Review query patterns and index usage
4. **Data Integrity**: Use foreign key constraints and validation

### Debug Commands

```bash
# Check database connection
python -c "from app.core.database import engine; print('Connection OK')"

# Verify model imports
python -c "from app.models import User; print('Models OK')"

# Test basic operations
python test_models.py
```

## Best Practices

1. **Always use migrations** for schema changes
2. **Test migrations** in development before production
3. **Monitor performance** and optimize queries regularly
4. **Implement proper error handling** for database operations
5. **Use transactions** for multi-step operations
6. **Follow naming conventions** for tables and columns
7. **Document schema changes** in migration messages
8. **Regular backups** and disaster recovery testing