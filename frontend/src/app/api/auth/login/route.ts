import { NextResponse } from 'next/server';

export async function GET() {
  // Extract domain from AUTH0_ISSUER_BASE_URL
  const issuerBaseUrl = process.env.AUTH0_ISSUER_BASE_URL;
  const domain = issuerBaseUrl?.replace('https://', '');
  
  // Simple login redirect
  const loginUrl = `https://${domain}/authorize?` +
    `response_type=code&` +
    `client_id=${process.env.AUTH0_CLIENT_ID}&` +
    `redirect_uri=${process.env.AUTH0_BASE_URL}/api/auth/callback&` +
    `scope=openid profile email`;
  
  return NextResponse.redirect(loginUrl);
}
// done hadiqa
