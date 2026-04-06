import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

/**
 * GET /api/auth/me
 * Returns current user session information
 */
export async function GET(request: NextRequest) {
  try {
    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get('appSession');

    if (!sessionCookie) {
      return NextResponse.json(
        { authenticated: false, user: null },
        { status: 200 }
      );
    }

    try {
      const session = JSON.parse(sessionCookie.value);
      
      return NextResponse.json(
        {
          authenticated: true,
          user: session.user || null,
          accessToken: session.accessToken ? '***' : null, // Don't send actual token
          idToken: session.idToken ? '***' : null,
        },
        { status: 200 }
      );
    } catch (parseError) {
      // Invalid session cookie
      return NextResponse.json(
        { authenticated: false, user: null, error: 'Invalid session' },
        { status: 200 }
      );
    }
  } catch (error) {
    console.error('Error in /api/auth/me:', error);
    return NextResponse.json(
      { authenticated: false, user: null, error: 'Internal server error' },
      { status: 500 }
    );
  }
}
