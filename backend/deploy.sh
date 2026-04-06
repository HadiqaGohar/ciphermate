#!/bin/bash

# CipherMate Backend Deployment Script for Google Cloud
set -e

# Configuration
PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}
REGION=${GOOGLE_CLOUD_REGION:-"us-central1"}
SERVICE_NAME="ciphermate-backend"

echo "🚀 Deploying CipherMate Backend to Google Cloud Run"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "Service: $SERVICE_NAME"

# Check if gcloud is installed and authenticated
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Check if user is authenticated
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated with gcloud. Please run 'gcloud auth login'"
    exit 1
fi

# Set the project
echo "📋 Setting project to $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required Google Cloud APIs"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com

# Build and deploy using Cloud Build
echo "🏗️ Building and deploying with Cloud Build"
gcloud builds submit --config cloudbuild.yaml

echo "✅ Deployment completed successfully!"
echo "🌐 Service URL: https://$SERVICE_NAME-$(gcloud config get-value project | tr ':' '-' | tr '.' '-')-$REGION.a.run.app"

# Show service status
echo "📊 Service status:"
gcloud run services describe $SERVICE_NAME --region=$REGION --format="table(status.url,status.conditions[0].type,status.conditions[0].status)"