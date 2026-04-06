#!/bin/bash

echo "🐘 Setting up PostgreSQL for CipherMate"
echo "======================================"

# Create PostgreSQL user with password
echo "Creating PostgreSQL user 'ciphermate'..."
sudo -u postgres createuser -s ciphermate 2>/dev/null || echo "User already exists"

# Set password for the user
echo "Setting password for user 'ciphermate'..."
sudo -u postgres psql -c "ALTER USER ciphermate PASSWORD 'ciphermate123';"

# Create database
echo "Creating database 'ciphermate'..."
sudo -u postgres createdb -O ciphermate ciphermate 2>/dev/null || echo "Database already exists"

# Test connection
echo "Testing connection..."
PGPASSWORD=ciphermate123 psql -U ciphermate -h localhost -d ciphermate -c "SELECT 1;" > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo "✅ PostgreSQL setup complete!"
    echo ""
    echo "Update your .env file with:"
    echo "DATABASE_URL=postgresql+asyncpg://ciphermate:ciphermate123@localhost:5432/ciphermate"
    echo ""
    echo "Then run: alembic upgrade head"
else
    echo "❌ Connection test failed. Please check PostgreSQL configuration."
fi