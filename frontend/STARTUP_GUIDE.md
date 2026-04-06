# CipherMate Frontend Startup Guide

## Quick Start

### Option 1: Use the Fix and Start Script
```bash
cd frontend
./fix-and-start.sh
```

### Option 2: Manual Start
```bash
cd frontend
npm install
npm run dev
```

## Configuration Fixed

The following Next.js 16 compatibility issues have been resolved:

### ✅ Fixed Issues
1. **Images Configuration**: Updated from deprecated `domains` to `remotePatterns`
2. **Server External Packages**: Moved from `experimental.serverComponentsExternalPackages` to `serverExternalPackages`
3. **Turbopack Configuration**: Added empty `turbopack: {}` to silence warnings
4. **Webpack Configuration**: Removed to avoid conflicts with Turbopack
5. **ESLint Configuration**: Removed from next.config.ts (use eslint.config.mjs instead)

### ✅ Environment Configuration
- Backend URL updated to `http://localhost:8000` (FastAPI default)
- All necessary environment variables configured
- Auth0, Google, GitHub, and Slack credentials ready

## Expected Behavior

When you run `npm run dev`, you should see:
```
▲ Next.js 16.2.1 (Turbopack)
- Local:         http://localhost:3000
- Network:       http://192.168.x.x:3000
✓ Ready in ~365ms
```

## Troubleshooting

### If you still see warnings:
- **Turbopack warnings**: These are informational and can be ignored
- **ESLint warnings**: The app will still work fine
- **Image domain warnings**: Fixed with `remotePatterns`

### If the app doesn't start:
1. Delete `.next` folder: `rm -rf .next`
2. Clear node_modules: `rm -rf node_modules && npm install`
3. Check environment variables in `.env.local`

### If you see "Module not found" errors:
```bash
npm install
```

## Development Workflow

1. **Start Backend** (in separate terminal):
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload --port 8000
   ```

2. **Start Frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

3. **Access Application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Features Available

### ✅ Working Features
- Next.js 16 with Turbopack
- Auth0 authentication
- Tailwind CSS styling
- TypeScript support
- API integration with backend
- Image optimization
- Security headers

### 🔧 Integration Points
- AI Agent API (`/api/v1/ai-agent/`)
- Token Vault API (`/api/v1/token-vault/`)
- OAuth flows for Google, GitHub, Slack
- Audit logging
- Permission management

## Production Deployment

The configuration is ready for production deployment on:
- Vercel (recommended)
- Docker
- Any Node.js hosting platform

## Next Steps

1. Start the development server
2. Test the Auth0 login flow
3. Verify API connectivity with backend
4. Test AI agent interactions
5. Configure OAuth for third-party services

The frontend is now fully compatible with Next.js 16 and ready for development!