#!/bin/bash

echo "Getting ngrok tunnel URLs..."

# Check if ngrok is running
if ! pgrep -f "ngrok" > /dev/null; then
    echo "Error: ngrok is not running. Please start ngrok first."
    echo "Run: ./start-ngrok.sh"
    exit 1
fi

# Get tunnel information
TUNNELS=$(curl -s http://localhost:4040/api/tunnels 2>/dev/null)

if [ $? -ne 0 ]; then
    echo "Error: Could not connect to ngrok API. Make sure ngrok is running."
    exit 1
fi

# Extract URLs
FRONTEND_URL=$(echo "$TUNNELS" | jq -r '.tunnels[] | select(.config.addr | contains("3000")) | .public_url' | head -1)
BACKEND_URL=$(echo "$TUNNELS" | jq -r '.tunnels[] | select(.config.addr | contains("8080")) | .public_url' | head -1)

echo ""
echo "=== NGROK TUNNEL URLS ==="
echo "Frontend URL: $FRONTEND_URL"
echo "Backend URL: $BACKEND_URL"
echo ""

echo "=== UPDATE YOUR AUTH0 CONFIGURATION ==="
echo "In your Auth0 Dashboard, update these URLs:"
echo ""
echo "Allowed Callback URLs:"
echo "  $FRONTEND_URL/api/auth/callback"
echo ""
echo "Allowed Logout URLs:"
echo "  $FRONTEND_URL"
echo ""
echo "Allowed Web Origins:"
echo "  $FRONTEND_URL"
echo ""
echo "Allowed Origins (CORS):"
echo "  $FRONTEND_URL"
echo ""

echo "=== UPDATE YOUR .env.local FILE ==="
echo "Update your frontend/.env.local file with:"
echo "AUTH0_BASE_URL=$FRONTEND_URL"
echo ""

# Save URLs to a file for easy access
cat > ngrok-urls.txt << EOF
FRONTEND_URL=$FRONTEND_URL
BACKEND_URL=$BACKEND_URL
EOF

echo "URLs saved to ngrok-urls.txt"