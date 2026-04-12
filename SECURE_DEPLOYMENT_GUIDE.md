# Secure Deployment Guide for CipherMate

## 🚨 Security Issue Fixed

**Problem**: GitHub detected sensitive data in commit and blocked push:
- Google OAuth Client ID & Secret
- Slack API Token  
- Auth0 credentials

**Solution**: Removed all sensitive data from repository files and created secure templates.

## 📁 File Structure (Secure)

### ✅ Safe to Commit:
```
├── .env.example              # Template with placeholder values
├── .env.template            # Template with placeholder values  
├── backend/.env.example     # Backend template
├── backend/.env.template    # Backend template
├── frontend/.env.local.example # Frontend template
├── .gitignore              # Protects sensitive files
```

### ❌ Never Commit (Protected by .gitignore):
```
├── .env                    # Actual environment variables
├── .env.local             # Local environment variables
├── .env.production        # Production environment variables
├── backend/.env           # Backend actual config
├── backend/.env.local     # Backend local config
├── frontend/.env.local    # Frontend actual config
```

## 🔐 Setting Up Secure Environment

### Step 1: Copy Templates
```bash
# Backend
cp backend/.env.example backend/.env
cp backend/.env.example backend/.env.local

# Frontend  
cp frontend/.env.local.example frontend/.env.local
```

### Step 2: Add Your Actual Credentials
Edit the copied files with your real values:

**Backend (.env):**
```env
# Replace these with your actual values:
AUTH0_DOMAIN=your-actual-domain.auth0.com
AUTH0_CLIENT_ID=your_actual_client_id
AUTH0_CLIENT_SECRET=your_actual_client_secret
GEMINI_API_KEY=your_actual_gemini_key
GOOGLE_CLIENT_ID=your_actual_google_client_id
GOOGLE_CLIENT_SECRET=your_actual_google_secret
```

**Frontend (.env.local):**
```env
# Replace these with your actual values:
AUTH0_ISSUER_BASE_URL=https://your-actual-domain.auth0.com
AUTH0_CLIENT_ID=your_actual_client_id
AUTH0_CLIENT_SECRET=your_actual_client_secret
NEXT_PUBLIC_API_URL=http://localhost:8080
```

## 🚀 Safe Deployment Process

### Local Development:
```bash
# 1. Setup environment
./fix-all-issues.sh  # Select option 1 (Setup templates)

# 2. Add your credentials to the generated files
# Edit backend/.env.local and frontend/.env.local.dev

# 3. Switch to local config
./switch-env.sh  # Select option 1 (Local)

# 4. Start development
cd backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
cd frontend && npm run dev
```

### Production Deployment:

#### Backend (Google Cloud Run):
```bash
# 1. Set environment variables in Cloud Run (not in files!)
gcloud run deploy ciphermate-backend \
  --source ./backend \
  --set-env-vars="AUTH0_DOMAIN=your-domain.auth0.com" \
  --set-env-vars="AUTH0_CLIENT_ID=your-client-id" \
  --set-env-vars="AUTH0_CLIENT_SECRET=your-client-secret" \
  --set-env-vars="GEMINI_API_KEY=your-gemini-key"
```

#### Frontend (Vercel):
```bash
# 1. Set environment variables in Vercel dashboard or CLI
vercel env add AUTH0_DOMAIN
vercel env add AUTH0_CLIENT_ID  
vercel env add AUTH0_CLIENT_SECRET
vercel env add NEXT_PUBLIC_API_URL

# 2. Deploy
vercel --prod
```

## 🔒 Environment Variable Management

### For Google Cloud Run:
```bash
# Set secrets using Secret Manager
gcloud secrets create auth0-client-secret --data-file=- <<< "your-secret"

# Use in Cloud Run
gcloud run deploy ciphermate-backend \
  --set-env-vars="AUTH0_CLIENT_SECRET_FILE=/secrets/auth0-client-secret"
```

### For Vercel:
```bash
# Set via CLI
vercel env add AUTH0_CLIENT_SECRET production

# Or via dashboard:
# https://vercel.com/your-team/ciphermate/settings/environment-variables
```

## 📋 Credential Checklist

### Auth0 Setup:
- [ ] Create Auth0 application
- [ ] Set callback URLs: `https://your-domain.vercel.app/api/auth/callback`
- [ ] Set logout URLs: `https://your-domain.vercel.app`
- [ ] Set web origins: `https://your-domain.vercel.app`
- [ ] Copy Domain, Client ID, Client Secret

### Google OAuth Setup:
- [ ] Create Google Cloud project
- [ ] Enable Google+ API
- [ ] Create OAuth 2.0 credentials
- [ ] Set authorized origins: `https://your-domain.vercel.app`
- [ ] Copy Client ID and Secret

### Gemini API Setup:
- [ ] Go to Google AI Studio
- [ ] Create API key
- [ ] Restrict key to specific APIs
- [ ] Copy API key

## 🧪 Testing Secure Setup

### Test Local Environment:
```bash
# Check environment variables are loaded
node -e "console.log('Auth0 Domain:', process.env.AUTH0_DOMAIN)"

# Test backend connection
curl http://localhost:8080/health

# Test frontend
curl http://localhost:3000
```

### Test Production Environment:
```bash
# Test backend
curl https://your-backend-url.run.app/health

# Test frontend  
curl https://your-frontend-url.vercel.app
```

## 🚨 Security Best Practices

### 1. Never Commit Secrets:
```bash
# Always check before committing
git diff --cached

# Use git-secrets to prevent accidents
git secrets --install
git secrets --register-aws
```

### 2. Rotate Credentials Regularly:
- Change Auth0 client secrets monthly
- Rotate API keys quarterly  
- Update database passwords regularly

### 3. Use Environment-Specific Configs:
- Development: Use test/sandbox credentials
- Staging: Use limited production credentials
- Production: Use full production credentials

### 4. Monitor for Exposed Secrets:
- Enable GitHub secret scanning
- Use tools like GitGuardian
- Monitor Auth0 logs for suspicious activity

## 🔄 Safe Git Workflow

### Before Committing:
```bash
# 1. Check for secrets
git diff --cached | grep -i "secret\|key\|token\|password"

# 2. Verify .gitignore is working
git status --ignored

# 3. Use safe commit message
git commit -m "feat: add secure environment templates"
```

### If You Accidentally Commit Secrets:
```bash
# 1. Remove from history (DANGEROUS - coordinate with team)
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/secret/file' \
  --prune-empty --tag-name-filter cat -- --all

# 2. Force push (DANGEROUS)
git push origin --force --all

# 3. Rotate all exposed credentials immediately
```

## 📞 Emergency Response

### If Secrets Are Exposed:
1. **Immediately rotate all exposed credentials**
2. **Revoke API keys in respective dashboards**
3. **Check logs for unauthorized access**
4. **Update all deployment environments**
5. **Notify team members**

### Contact Information:
- Auth0 Support: https://support.auth0.com
- Google Cloud Support: https://cloud.google.com/support
- Vercel Support: https://vercel.com/support

## ✅ Deployment Checklist

### Pre-Deployment:
- [ ] All secrets removed from code
- [ ] Environment variables set in deployment platforms
- [ ] .gitignore protecting sensitive files
- [ ] Credentials rotated from development
- [ ] Auth0 URLs updated for production domain

### Post-Deployment:
- [ ] Health checks passing
- [ ] Authentication flow working
- [ ] API connections successful
- [ ] Logs showing no errors
- [ ] Security monitoring enabled

Now you can safely commit and deploy without exposing sensitive data! 🎉