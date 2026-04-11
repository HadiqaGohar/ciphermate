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
    const response = await fetch(`${BACKEND_URL}/api/v1/audit/export?${queryString}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${session.accessToken}`,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Unknown error' }));
      return NextResponse.json(
        { error: errorData.detail || 'Failed to export audit data' },
        { status: response.status }
      );
    }

    // Get the content type and filename from the backend response
    const contentType = response.headers.get('content-type') || 'application/octet-stream';
    const contentDisposition = response.headers.get('content-disposition');
    
    // Stream the response from backend to client
    const data = await response.arrayBuffer();
    
    const headers: Record<string, string> = {
      'Content-Type': contentType,
    };
    
    if (contentDisposition) {
      headers['Content-Disposition'] = contentDisposition;
    }

    return new NextResponse(data, {
      status: 200,
      headers,
    });

  } catch (error) {
    console.error('Error exporting audit data:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}