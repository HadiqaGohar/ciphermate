#!/bin/bash

# Google Cloud Secrets Manager setup for CipherMate
set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-"your-project-id"}

echo "🔐 Setting up secrets in Google Cloud Secret Manager"
echo "Project: $PROJECT_ID"

# Check if gcloud is installed and authenticated
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed. Please install it first."
    exit 1
fi

# Set the project
gcloud config set project $PROJECT_ID

# Enable Secret Manager API
echo "🔧 Enabling Secret Manager API"
gcloud services enable secretmanager.googleapis.com

# Function to create or update secret
create_or_update_secret() {
    local secret_name=$1
    local secret_value=$2
    
    if gcloud secrets describe $secret_name >/dev/null 2>&1; then
        echo "📝 Updating existing secret: $secret_name"
        echo -n "$secret_value" | gcloud secrets versions add $secret_name --data-file=-
    else
        echo "🆕 Creating new secret: $secret_name"
        echo -n "$secret_value" | gcloud secrets create $secret_name --data-file=-
    fi
}

# Prompt for secrets if not provided as environment variables
echo "📋 Please provide the following secrets (or set them as environment variables):"

# Database URL
if [ -z "$DATABASE_URL" ]; then
    echo -n "Database URL (Supabase PostgreSQL): "
    read -s DATABASE_URL
    echo
fi
create_or_update_secret "DATABASE_URL" "$DATABASE_URL"

# Auth0 Configuration
if [ -z "$AUTH0_DOMAIN" ]; then
    echo -n "Auth0 Domain: "
    read AUTH0_DOMAIN
fi
create_or_update_secret "AUTH0_DOMAIN" "$AUTH0_DOMAIN"

if [ -z "$AUTH0_CLIENT_ID" ]; then
    echo -n "Auth0 Client ID: "
    read AUTH0_CLIENT_ID
fi
create_or_update_secret "AUTH0_CLIENT_ID" "$AUTH0_CLIENT_ID"

if [ -z "$AUTH0_CLIENT_SECRET" ]; then
    echo -n "Auth0 Client Secret: "
    read -s AUTH0_CLIENT_SECRET
    echo
fi
create_or_update_secret "AUTH0_CLIENT_SECRET" "$AUTH0_CLIENT_SECRET"

if [ -z "$AUTH0_AUDIENCE" ]; then
    echo -n "Auth0 Audience: "
    read AUTH0_AUDIENCE
fi
create_or_update_secret "AUTH0_AUDIENCE" "$AUTH0_AUDIENCE"

# AI API Keys
if [ -z "$GEMINI_API_KEY" ]; then
    echo -n "Gemini API Key: "
    read -s GEMINI_API_KEY
    echo
fi
create_or_update_secret "GEMINI_API_KEY" "$GEMINI_API_KEY"

# OAuth Client Secrets
if [ -z "$GOOGLE_CLIENT_ID" ]; then
    echo -n "Google OAuth Client ID: "
    read GOOGLE_CLIENT_ID
fi
create_or_update_secret "GOOGLE_CLIENT_ID" "$GOOGLE_CLIENT_ID"

if [ -z "$GOOGLE_CLIENT_SECRET" ]; then
    echo -n "Google OAuth Client Secret: "
    read -s GOOGLE_CLIENT_SECRET
    echo
fi
create_or_update_secret "GOOGLE_CLIENT_SECRET" "$GOOGLE_CLIENT_SECRET"

if [ -z "$GITHUB_CLIENT_ID" ]; then
    echo -n "GitHub OAuth Client ID: "
    read GITHUB_CLIENT_ID
fi
create_or_update_secret "GITHUB_CLIENT_ID" "$GITHUB_CLIENT_ID"

if [ -z "$GITHUB_CLIENT_SECRET" ]; then
    echo -n "GitHub OAuth Client Secret: "
    read -s GITHUB_CLIENT_SECRET
    echo
fi
create_or_update_secret "GITHUB_CLIENT_SECRET" "$GITHUB_CLIENT_SECRET"

if [ -z "$SLACK_CLIENT_ID" ]; then
    echo -n "Slack OAuth Client ID: "
    read SLACK_CLIENT_ID
fi
create_or_update_secret "SLACK_CLIENT_ID" "$SLACK_CLIENT_ID"

if [ -z "$SLACK_CLIENT_SECRET" ]; then
    echo -n "Slack OAuth Client Secret: "
    read -s SLACK_CLIENT_SECRET
    echo
fi
create_or_update_secret "SLACK_CLIENT_SECRET" "$SLACK_CLIENT_SECRET"

echo "✅ All secrets have been configured in Google Cloud Secret Manager"
echo "🔍 You can view them with: gcloud secrets list"