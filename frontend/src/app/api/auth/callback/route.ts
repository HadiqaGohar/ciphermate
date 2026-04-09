import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    console.log('Auth callback received');
    
    const { searchParams } = new URL(request.url);
    const code = searchParams.get('code');
    const error = searchParams.get('error');
    
    // Handle Auth0 errors
    if (error) {
      console.error('Auth0 error:', error);
      return NextResponse.redirect(new URL(`/auth/login?error=${error}`, request.url));
    }
    
    // Check if we have an authorization code
    if (!code) {
      console.error('No authorization code received');
      return NextResponse.redirect(new URL('/auth/login?error=no_code', request.url));
    }
    
    // Exchange code for tokens
    const tokenResponse = await fetch(`${process.env.AUTH0_ISSUER_BASE_URL}/oauth/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        grant_type: 'authorization_code',
        client_id: process.env.AUTH0_CLIENT_ID,
        client_secret: process.env.AUTH0_CLIENT_SECRET,
        code: code,
        redirect_uri: `${process.env.AUTH0_BASE_URL}/api/auth/callback`,
      }),
    });
    
    if (!tokenResponse.ok) {
      console.error('Token exchange failed:', await tokenResponse.text());
      return NextResponse.redirect(new URL('/auth/login?error=token_exchange_failed', request.url));
    }
    
    const tokens = await tokenResponse.json();
    
    // Get user info
    const userResponse = await fetch(`${process.env.AUTH0_ISSUER_BASE_URL}/userinfo`, {
      headers: {
        'Authorization': `Bearer ${tokens.access_token}`,
      },
    });
    
    if (!userResponse.ok) {
      console.error('Failed to get user info');
      return NextResponse.redirect(new URL('/auth/login?error=user_info_failed', request.url));
    }
    
    const user = await userResponse.json();
    
    // Create session data
    const sessionData = {
      user: {
        sub: user.sub,
        name: user.name,
        email: user.email,
        picture: user.picture,
      },
      accessToken: tokens.access_token,
      refreshToken: tokens.refresh_token,
      expiresAt: Date.now() + (tokens.expires_in * 1000),
      authenticated: true,
    };
    
    // Create response and set session cookie
    const response = NextResponse.redirect(new URL('/dashboard', request.url));
    
    // Set session cookie
    response.cookies.set('appSession', JSON.stringify(sessionData), {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: tokens.expires_in || 3600, // 1 hour default
      path: '/',
    });
    
    // Set additional auth cookies for compatibility
    response.cookies.set('auth0.is.authenticated', 'true', {
      httpOnly: false,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: tokens.expires_in || 3600,
      path: '/',
    });
    
    console.log('Login successful for user:', user.email);
    return response;
    
  } catch (error) {
    console.error('Callback error:', error);
    return NextResponse.redirect(new URL('/auth/login?error=callback_error', request.url));
  }
}