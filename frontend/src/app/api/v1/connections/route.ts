import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // For now, return mock data since DISABLE_AGENTS=true
    const mockConnections = [
      {
        id: "1",
        service_name: "Gmail",
        service_type: "email",
        status: "active",
        created_at: new Date().toISOString()
      },
      {
        id: "2", 
        service_name: "GitHub",
        service_type: "code",
        status: "active",
        created_at: new Date().toISOString()
      }
    ];

    return NextResponse.json(mockConnections);
  } catch (error) {
    console.error('Error fetching connections:', error);
    return NextResponse.json({ error: 'Failed to fetch connections' }, { status: 500 });
  }
}