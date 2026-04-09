import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  const { pathname } = new URL(request.url);
  const segments = pathname.split('/');
  const action = segments[segments.length - 1];

  // Extract domain from AUTH0_ISSUER_BASE_URL
  const issuerBaseUrl = process.env.AUTH0_ISSUER_BASE_URL;
  const domain = issuerBaseUrl?.replace('https://', '');

  // For now, let's create a simple redirect-based auth flow
  switch (action) {
    case 'login':
      // Redirect to Auth0 login
      const loginUrl = `https://${domain}/authorize?` +
        `response_type=code&` +
        `client_id=${process.env.AUTH0_CLIENT_ID}&` +
        `redirect_uri=${process.env.AUTH0_BASE_URL}/api/auth/callback&` +
        `scope=openid profile email`;
      return NextResponse.redirect(loginUrl);
      
    case 'logout':
      // Clear session cookies and redirect to Auth0 logout
      const logoutUrl = `https://${domain}/v2/logout?` +
        `client_id=${process.env.AUTH0_CLIENT_ID}&` +
        `returnTo=${encodeURIComponent(process.env.AUTH0_BASE_URL || 'http://localhost:3000')}`;
      
      const logoutResponse = NextResponse.redirect(logoutUrl);
      
      // Clear all authentication-related cookies
      const cookiesToClear = [
        'appSession',
        'auth0.is.authenticated',
        'auth0.session', 
        'auth-token',
        'access-token',
        'refresh-token'
      ];
      
      cookiesToClear.forEach(cookieName => {
        logoutResponse.cookies.set(cookieName, '', {
          expires: new Date(0),
          path: '/',
          httpOnly: true,
          secure: process.env.NODE_ENV === 'production',
          sameSite: 'lax'
        });
      });
      
      return logoutResponse;
      
    case 'callback':
      // Redirect to dedicated callback handler
      return NextResponse.redirect(new URL('/api/auth/callback' + request.nextUrl.search, request.url));
      
    case 'me':
      // Redirect to dedicated me endpoint
      return NextResponse.redirect(new URL('/api/auth/me', request.url));
      
    default:
      return new NextResponse('Not Found', { status: 404 });
  }
}

export const POST = GET;