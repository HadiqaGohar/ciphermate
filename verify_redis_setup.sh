#!/bin/bash

echo "🔧 CipherMate Redis Setup Verification"
echo "======================================"

# Check if Redis is installed
echo "1. Checking Redis installation..."
if command -v redis-cli &> /dev/null; then
    echo "✅ Redis CLI is installed"
    redis-cli --version
else
    echo "❌ Redis CLI is not installed"
    exit 1
fi

# Check if Redis server is running
echo ""
echo "2. Checking Redis server status..."
if redis-cli ping &> /dev/null; then
    echo "✅ Redis server is running and responding"
else
    echo "❌ Redis server is NOT running"
    echo "Try: sudo systemctl start redis-server"
    exit 1
fi

# Test Redis operations
echo ""
echo "3. Testing Redis operations..."
redis-cli set ciphermate_test "Hello from CipherMate!" &> /dev/null
if redis-cli get ciphermate_test | grep -q "Hello from CipherMate!"; then
    echo "✅ Redis read/write operations working"
    redis-cli del ciphermate_test &> /dev/null
else
    echo "❌ Redis read/write operations failed"
    exit 1
fi

# Get Redis info
echo ""
echo "4. Redis server information:"
echo "   Version: $(redis-cli INFO server | grep redis_version | cut -d: -f2 | tr -d '\r')"
echo "   Memory: $(redis-cli INFO memory | grep used_memory_human | cut -d: -f2 | tr -d '\r')"
echo "   Port: 6379"
echo "   Host: 127.0.0.1"

# Check if Redis is enabled to start on boot
echo ""
echo "5. Checking Redis auto-start..."
if systemctl is-enabled redis-server &> /dev/null; then
    echo "✅ Redis is enabled to start on boot"
else
    echo "⚠️  Redis is not enabled for auto-start"
    echo "   Run: sudo systemctl enable redis-server"
fi

echo ""
echo "🎉 Redis Setup Complete!"
echo "======================================"
echo "✅ Redis is installed and running"
echo "✅ Redis is accessible on localhost:6379"
echo "✅ Your CipherMate backend can now use Redis for caching"
echo ""
echo "📝 Next Steps:"
echo "1. Restart your CipherMate backend"
echo "2. Check backend logs - Redis connection errors should be gone"
echo "3. Your app now has full caching capabilities!"
echo ""
echo "🔄 To restart backend:"
echo "   cd backend"
echo "   uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload"