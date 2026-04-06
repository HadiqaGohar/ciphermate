#!/bin/bash
set -e

echo "🚀 Deploying CipherMate Backend to Cloud Run..."

# Set project and region
PROJECT_ID="gemini-cli-478208"
REGION="europe-west1"
SERVICE_NAME="ciphermate"

echo "📦 Building and deploying..."

# Deploy directly from source with explicit configuration
gcloud run deploy $SERVICE_NAME \
    --source . \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --memory 1Gi \
    --cpu 1 \
    --timeout 300 \
    --port 8080 \
    --set-env-vars="PORT=8080,DISABLE_DATABASE=true,DISABLE_REDIS=true,APP_ENV=production" \
    --max-instances 10 \
    --min-instances 0 \
    --concurrency 80 \
    --no-use-http2 \
    --execution-environment gen2

echo "✅ Deployment complete!"

# Get the service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format='value(status.url)')
echo "🌐 Service URL: $SERVICE_URL"

# Test the deployment
echo "🧪 Testing deployment..."
curl -f "$SERVICE_URL/health" || echo "❌ Health check failed"
curl -f "$SERVICE_URL/" || echo "❌ Root endpoint failed"

echo "🎉 Deployment and testing complete!"