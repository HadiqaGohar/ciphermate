// Quick test to verify Auth0 setup
console.log('Auth0 Environment Variables:');
console.log('AUTH0_SECRET:', process.env.AUTH0_SECRET ? '✓ Set' : '✗ Missing');
console.log('AUTH0_BASE_URL:', process.env.AUTH0_BASE_URL);
console.log('AUTH0_ISSUER_BASE_URL:', process.env.AUTH0_ISSUER_BASE_URL);
console.log('AUTH0_CLIENT_ID:', process.env.AUTH0_CLIENT_ID ? '✓ Set' : '✗ Missing');
console.log('AUTH0_CLIENT_SECRET:', process.env.AUTH0_CLIENT_SECRET ? '✓ Set' : '✗ Missing');