import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export async function GET(request: NextRequest) {
  try {
    // Get session from cookies
    const cookieStore = await cookies();
    const sessionCookie = cookieStore.get('appSession');

    if (!sessionCookie?.value) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    let session;
    try {
      session = JSON.parse(sessionCookie.value);
    } catch {
      return NextResponse.json(
        { error: 'Invalid session' },
        { status: 401 }
      );
    }

    if (!session?.accessToken) {
      return NextResponse.json(
        { error: 'Unauthorized' },
        { status: 401 }
      );
    }

    const { searchParams } = new URL(request.url);
    const queryString = searchParams.toString();

    // Forward request to backend with auth
    const response = await fetch(`${BACKEND_URL}/api/v1/audit/summary?${queryString}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.accessToken}`,
      },
    });

    if (!response.ok) {
      // Return fallback data if backend fails
      return NextResponse.json({
        period_days: 30,
        start_date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
        action_counts: {},
        service_usage: {},
        security_events: []
      });
    }

    const data = await response.json();
    
    // Ensure the response has the expected structure with defaults
    return NextResponse.json({
      period_days: data.period_days || 30,
      start_date: data.start_date || new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      action_counts: data.action_counts || {},
      service_usage: data.service_usage || {},
      security_events: data.security_events || []
    });

  } catch (error) {
    console.error('Error fetching audit summary:', error);
    
    // Return fallback data on error
    return NextResponse.json({
      period_days: 30,
      start_date: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000).toISOString().split('T')[0],
      action_counts: {},
      service_usage: {},
      security_events: []
    });
  }
}