# CipherMate Production Deployment Guide

This guide covers the complete production deployment of CipherMate to Google Cloud Platform and Vercel.

## Prerequisites

### Required Tools
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install)
- [Node.js 18+](https://nodejs.org/)
- [Vercel CLI](https://vercel.com/cli) (optional)
- [Git](https://git-scm.com/)

### Required Accounts
- Google Cloud Platform account with billing enabled
- Vercel account
- Supabase account
- Auth0 account with Token Vault feature enabled

## Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Vercel        │    │  Google Cloud    │    │   Supabase      │
│   (Frontend)    │◄──►│  (Backend API)   │◄──►│  (Database)     │
│                 │    │                  │    │                 │
│ Next.js App     │    │ Cloud Run        │    │ PostgreSQL      │
│ Auth0 SDK       │    │ FastAPI          │    │ Row Level       │
│ React UI        │    │ Token Vault      │    │ Security        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌────────▼────────┐             │
         │              │ Google Cloud    │             │
         │              │ Secret Manager  │             │
         │              │                 │             │
         └──────────────► API Keys &      │◄────────────┘
                        │ Secrets         │
                        └─────────────────┘
```

## Step 1: Database Setup (Supabase)

### 1.1 Create Supabase Project
1. Go to [Supabase](https://supabase.com) and create a new project
2. Choose a region close to your users
3. Set a strong database password
4. Wait for the project to be ready

### 1.2 Configure Database
1. Go to the SQL Editor in your Supabase dashboard
2. Run the setup script:
   ```bash
   cat backend/setup-supabase.sql
   ```
3. Copy and paste the entire content into the SQL editor and execute
4. Verify tables are created in the Table Editor

### 1.3 Get Database Connection String
1. Go to Settings → Database
2. Copy the connection string (URI format)
3. Replace `[YOUR-PASSWORD]` with your actual password
4. Save this for later use

## Step 2: Auth0 Configuration

### 2.1 Create Auth0 Application
1. Go to [Auth0 Dashboard](https://manage.auth0.com)
2. Create a new Single Page Application
3. Configure the following settings:
   - **Allowed Callback URLs**: `https://your-domain.vercel.app/api/auth/callback`
   - **Allowed Logout URLs**: `https://your-domain.vercel.app`
   - **Allowed Web Origins**: `https://your-domain.vercel.app`

### 2.2 Enable Token Vault
1. Go to Applications → APIs → Auth0 Management API
2. Enable the Token Vault feature
3. Configure the necessary scopes for your application

### 2.3 Configure OAuth Connections
Set up OAuth connections for:
- Google (Calendar, Gmail, Drive)
- GitHub
- Slack

## Step 3: Backend Deployment (Google Cloud)

### 3.1 Setup Google Cloud Project
```bash
# Create a new project
gcloud projects create ciphermate-prod --name="CipherMate Production"

# Set the project
gcloud config set project ciphermate-prod

# Enable billing (required for Cloud Run)
# Do this through the Google Cloud Console
```

### 3.2 Configure Secrets
```bash
# Navigate to backend directory
cd backend

# Run the secrets setup script
./setup-secrets.sh

# Follow the prompts to enter your secrets:
# - Database URL (from Supabase)
# - Auth0 configuration
# - API keys (Gemini, etc.)
# - OAuth client secrets
```

### 3.3 Deploy Backend
```bash
# Make sure you're in the backend directory
cd backend

# Deploy using the deployment script
./deploy.sh

# The script will:
# 1. Enable required Google Cloud APIs
# 2. Build the Docker image
# 3. Deploy to Cloud Run
# 4. Configure environment variables and secrets
```

### 3.4 Verify Backend Deployment
```bash
# Get the service URL
gcloud run services describe ciphermate-backend --region=us-central1 --format="value(status.url)"

# Test the health endpoint
curl https://your-service-url.a.run.app/health
```

## Step 4: Frontend Deployment (Vercel)

### 4.1 Prepare Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Build the application
npm run build
```

### 4.2 Deploy to Vercel

#### Option A: Using Vercel CLI
```bash
# Install Vercel CLI
npm install -g vercel

# Login to Vercel
vercel login

# Deploy
vercel --prod

# Set environment variables
vercel env add AUTH0_SECRET
vercel env add AUTH0_BASE_URL
vercel env add AUTH0_ISSUER_BASE_URL
vercel env add AUTH0_CLIENT_ID
vercel env add AUTH0_CLIENT_SECRET
vercel env add NEXT_PUBLIC_BACKEND_URL
```

#### Option B: Using Vercel Dashboard
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Import your GitHub repository
3. Configure environment variables:
   - `AUTH0_SECRET`: Generate a random 32-character string
   - `AUTH0_BASE_URL`: Your Vercel domain (e.g., `https://ciphermate.vercel.app`)
   - `AUTH0_ISSUER_BASE_URL`: Your Auth0 domain
   - `AUTH0_CLIENT_ID`: From Auth0 application settings
   - `AUTH0_CLIENT_SECRET`: From Auth0 application settings
   - `NEXT_PUBLIC_BACKEND_URL`: Your Google Cloud Run service URL

### 4.3 Update Auth0 Configuration
Update your Auth0 application settings with the actual Vercel domain:
- **Allowed Callback URLs**: `https://your-actual-domain.vercel.app/api/auth/callback`
- **Allowed Logout URLs**: `https://your-actual-domain.vercel.app`
- **Allowed Web Origins**: `https://your-actual-domain.vercel.app`

## Step 5: Configure Monitoring

### 5.1 Enable Google Cloud Monitoring
```bash
# Enable monitoring APIs
gcloud services enable monitoring.googleapis.com
gcloud services enable logging.googleapis.com

# Create monitoring policies (optional)
gcloud alpha monitoring policies create --policy-from-file=backend/monitoring.yaml
```

### 5.2 Set Up Uptime Checks
1. Go to Google Cloud Console → Monitoring → Uptime checks
2. Create uptime checks for:
   - Backend health endpoint: `https://your-service-url.a.run.app/health`
   - Frontend: `https://your-domain.vercel.app`

### 5.3 Configure Alerting
1. Set up notification channels (email, Slack, etc.)
2. Create alert policies for:
   - High error rates
   - High latency
   - Service downtime
   - Database connection issues

## Step 6: Security Configuration

### 6.1 Configure CORS
Update the backend CORS configuration in `app/core/config.py`:
```python
ALLOWED_ORIGINS = [
    "https://your-actual-domain.vercel.app",
    "https://your-custom-domain.com"  # if using custom domain
]
```

### 6.2 Set Up Custom Domain (Optional)
1. In Vercel, go to your project settings
2. Add your custom domain
3. Configure DNS records as instructed
4. Update Auth0 URLs to use the custom domain

### 6.3 Enable Security Headers
The frontend is configured with security headers in `vercel.json`. Verify they're working:
```bash
curl -I https://your-domain.vercel.app
```

## Step 7: Testing and Validation

### 7.1 End-to-End Testing
1. Visit your frontend URL
2. Test user authentication flow
3. Grant permissions to a service (e.g., Google Calendar)
4. Test AI agent interactions
5. Verify audit logging
6. Test permission revocation

### 7.2 Performance Testing
```bash
# Test backend performance
curl -w "@curl-format.txt" -o /dev/null -s https://your-service-url.a.run.app/health

# Create curl-format.txt with:
echo "     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n" > curl-format.txt
```

### 7.3 Security Testing
1. Test rate limiting
2. Verify JWT token validation
3. Test unauthorized access attempts
4. Verify secrets are not exposed in logs

## Step 8: Maintenance and Updates

### 8.1 Backend Updates
```bash
# Update backend
cd backend
./deploy.sh

# Check deployment status
gcloud run services describe ciphermate-backend --region=us-central1
```

### 8.2 Frontend Updates
```bash
# Update frontend
cd frontend
vercel --prod
```

### 8.3 Database Migrations
```bash
# Run database migrations (if using Alembic)
# This would typically be done through a Cloud Build trigger
# or manually through the Cloud Run console
```

## Troubleshooting

### Common Issues

#### Backend Won't Start
1. Check Cloud Run logs:
   ```bash
   gcloud logs read --service=ciphermate-backend --limit=50
   ```
2. Verify all secrets are properly configured
3. Check database connectivity

#### Frontend Authentication Issues
1. Verify Auth0 configuration matches Vercel domain
2. Check environment variables in Vercel dashboard
3. Verify `AUTH0_SECRET` is properly set

#### Database Connection Issues
1. Verify Supabase database is running
2. Check connection string format
3. Verify Row Level Security policies

#### CORS Issues
1. Update `ALLOWED_ORIGINS` in backend configuration
2. Redeploy backend after changes
3. Clear browser cache

### Monitoring and Logs

#### Backend Logs
```bash
# View recent logs
gcloud logs read --service=ciphermate-backend --limit=100

# Follow logs in real-time
gcloud logs tail --service=ciphermate-backend
```

#### Frontend Logs
1. Check Vercel dashboard → Functions tab
2. View real-time logs in Vercel CLI:
   ```bash
   vercel logs
   ```

#### Database Logs
1. Go to Supabase dashboard → Logs
2. Check for connection issues or query errors

## Cost Optimization

### Google Cloud
- Use Cloud Run's pay-per-request model
- Set appropriate CPU and memory limits
- Configure min/max instances based on usage
- Use Cloud Build triggers for automated deployments

### Vercel
- Optimize bundle size
- Use Vercel's edge functions for better performance
- Monitor bandwidth usage

### Supabase
- Monitor database usage
- Optimize queries with proper indexing
- Use connection pooling for better performance

## Security Best Practices

1. **Secrets Management**: Never commit secrets to version control
2. **Regular Updates**: Keep dependencies updated
3. **Monitoring**: Set up comprehensive monitoring and alerting
4. **Backup**: Regular database backups (Supabase handles this automatically)
5. **Access Control**: Use principle of least privilege for all services
6. **Audit Logging**: Comprehensive logging of all user actions
7. **Rate Limiting**: Protect against abuse and DoS attacks

## Support and Maintenance

### Regular Tasks
- [ ] Monitor application performance and errors
- [ ] Review security events and audit logs
- [ ] Update dependencies monthly
- [ ] Review and rotate secrets quarterly
- [ ] Test backup and recovery procedures
- [ ] Review and update monitoring alerts

### Emergency Procedures
1. **Service Outage**: Check Google Cloud Status and Vercel Status pages
2. **Security Incident**: Review audit logs and security events
3. **Data Issues**: Use Supabase point-in-time recovery if needed
4. **Performance Issues**: Scale Cloud Run instances or optimize queries

For additional support, refer to the documentation of each service:
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Vercel Documentation](https://vercel.com/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Auth0 Documentation](https://auth0.com/docs)