#!/bin/bash

# Start ngrok for frontend (port 3000)
echo "Starting ngrok for frontend on port 3000..."
ngrok http 3000 --log=stdout > ngrok-frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait a moment for ngrok to start
sleep 3

# Start ngrok for backend (port 8080)
echo "Starting ngrok for backend on port 8080..."
ngrok http 8080 --log=stdout > ngrok-backend.log 2>&1 &
BACKEND_PID=$!

echo "Ngrok processes started:"
echo "Frontend PID: $FRONTEND_PID"
echo "Backend PID: $BACKEND_PID"

echo ""
echo "To get the ngrok URLs, run:"
echo "curl -s http://localhost:4040/api/tunnels | jq '.tunnels[].public_url'"

echo ""
echo "To stop ngrok processes:"
echo "kill $FRONTEND_PID $BACKEND_PID"

# Save PIDs for later cleanup
echo "$FRONTEND_PID" > ngrok-frontend.pid
echo "$BACKEND_PID" > ngrok-backend.pid

wait