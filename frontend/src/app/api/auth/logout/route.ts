import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Extract domain from AUTH0_ISSUER_BASE_URL
    const issuerBaseUrl = process.env.AUTH0_ISSUER_BASE_URL;
    const domain = issuerBaseUrl?.replace('https://', '');
    
    // Create response with Auth0 logout redirect
    const logoutUrl = `https://${domain}/v2/logout?` +
      `client_id=${process.env.AUTH0_CLIENT_ID}&` +
      `returnTo=${encodeURIComponent(process.env.AUTH0_BASE_URL || 'http://localhost:3000')}`;
    
    const response = NextResponse.redirect(logoutUrl);
    
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
      response.cookies.set(cookieName, '', {
        expires: new Date(0),
        path: '/',
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax'
      });
    });
    
    return response;
  } catch (error) {
    console.error('Logout error:', error);
    // Fallback: redirect to home page with cleared cookies
    const response = NextResponse.redirect(new URL('/', request.url));
    
    // Still clear cookies even if Auth0 logout fails
    const cookiesToClear = [
      'appSession',
      'auth0.is.authenticated', 
      'auth0.session',
      'auth-token',
      'access-token',
      'refresh-token'
    ];
    
    cookiesToClear.forEach(cookieName => {
      response.cookies.set(cookieName, '', {
        expires: new Date(0),
        path: '/',
        httpOnly: true,
        secure: process.env.NODE_ENV === 'production',
        sameSite: 'lax'
      });
    });
    
    return response;
  }
}