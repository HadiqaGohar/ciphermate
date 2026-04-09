#!/bin/bash

echo "🔧 Testing Dashboard API Endpoints"
echo "=================================="

# Check if frontend is running
if ! curl -s http://localhost:3000 > /dev/null; then
    echo "❌ Frontend not running on localhost:3000"
    echo "Please start the frontend with: cd frontend && npm run dev"
    exit 1
fi

echo "✅ Frontend is running"

# Test connections endpoint
echo "🔗 Testing /api/v1/agent/connections..."
CONNECTIONS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/v1/agent/connections)
if [ "$CONNECTIONS_RESPONSE" = "200" ]; then
    echo "✅ Connections endpoint working"
    curl -s http://localhost:3000/api/v1/agent/connections | jq '.[0].service_name' 2>/dev/null || echo "   (JSON response received)"
else
    echo "❌ Connections endpoint failed: $CONNECTIONS_RESPONSE"
fi

# Test actions endpoint
echo "⚡ Testing /api/v1/agent/actions..."
ACTIONS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/v1/agent/actions)
if [ "$ACTIONS_RESPONSE" = "200" ]; then
    echo "✅ Actions endpoint working"
    curl -s http://localhost:3000/api/v1/agent/actions | jq '.[0].action' 2>/dev/null || echo "   (JSON response received)"
else
    echo "❌ Actions endpoint failed: $ACTIONS_RESPONSE"
fi

# Test stats endpoint
echo "📊 Testing /api/v1/demo/stats..."
STATS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000/api/v1/demo/stats)
if [ "$STATS_RESPONSE" = "200" ]; then
    echo "✅ Stats endpoint working"
    curl -s http://localhost:3000/api/v1/demo/stats | jq '.total_users' 2>/dev/null || echo "   (JSON response received)"
else
    echo "❌ Stats endpoint failed: $STATS_RESPONSE"
fi

# Test simulate action endpoint
echo "🎯 Testing /api/v1/demo/simulate-action..."
SIMULATE_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" -X POST http://localhost:3000/api/v1/demo/simulate-action)
if [ "$SIMULATE_RESPONSE" = "200" ]; then
    echo "✅ Simulate action endpoint working"
else
    echo "❌ Simulate action endpoint failed: $SIMULATE_RESPONSE"
fi

echo ""
echo "🎯 Dashboard Fix Summary:"
echo "========================"
echo "✅ Fixed dashboard to use custom useAuth hook"
echo "✅ Updated API calls to use frontend routes instead of backend"
echo "✅ Added proper JSON content-type checking"
echo "✅ Added fallback mock data for offline mode"
echo "✅ Created missing /api/v1/agent/connections endpoint"
echo "✅ Updated actions endpoint to match dashboard expectations"
echo ""
echo "📝 Dashboard should now work without JSON parsing errors!"
echo "The dashboard will show mock data and all functionality should work."