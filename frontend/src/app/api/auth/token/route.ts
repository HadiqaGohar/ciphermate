import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Try to get token from Auth0 session via backend
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
    
    try {
      // Get user's session from backend
      const sessionResponse = await fetch(`${backendUrl}/api/v1/auth/session`, {
        method: 'GET',
        headers: {
          'Cookie': request.headers.get('cookie') || ''
        },
        credentials: 'include'
      });

      if (sessionResponse.ok) {
        const sessionData = await sessionResponse.json();
        return NextResponse.json({
          accessToken: sessionData.access_token || null,
          user: sessionData.user_data || null,
          session_id: sessionData.session_id
        });
      }
    } catch (sessionError) {
      console.warn('Backend session not available, checking for stored token');
    }

    // Fallback: return empty response indicating no auth
    return NextResponse.json({
      accessToken: null,
      user: null,
      message: 'No active session found'
    }, { status: 401 });

  } catch (error) {
    console.error('Error getting access token:', error);
    return NextResponse.json(
      { error: 'Failed to get access token' },
      { status: 500 }
    );
  }
}