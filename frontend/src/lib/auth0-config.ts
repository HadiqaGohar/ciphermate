// Auth0 configuration helper
export const auth0Config = {
  domain: process.env.AUTH0_ISSUER_BASE_URL?.replace('https://', '') || '',
  clientId: process.env.AUTH0_CLIENT_ID || '',
  clientSecret: process.env.AUTH0_CLIENT_SECRET || '',
  baseURL: process.env.AUTH0_BASE_URL || 'http://localhost:3000',
  secret: process.env.AUTH0_SECRET || '',
  issuerBaseURL: process.env.AUTH0_ISSUER_BASE_URL || '',
  routes: {
    callback: '/api/auth/callback',
    postLogoutRedirect: '/'
  }
};

// Validate configuration
export function validateAuth0Config() {
  const required = ['domain', 'clientId', 'clientSecret', 'baseURL', 'secret', 'issuerBaseURL'];
  const missing = required.filter(key => !auth0Config[key as keyof typeof auth0Config]);
  
  if (missing.length > 0) {
    console.error('Missing Auth0 configuration:', missing);
    return false;
  }
  
  return true;
}