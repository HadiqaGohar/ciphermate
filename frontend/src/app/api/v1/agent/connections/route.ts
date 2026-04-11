import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Return mock connections data
    const mockConnections = [
      {
        id: "1",
        service_name: "Gmail",
        service_type: "Email",
        status: "active",
        created_at: new Date(Date.now() - 86400000).toISOString(), // 1 day ago
      },
      {
        id: "2",
        service_name: "Slack",
        service_type: "Communication", 
        status: "active",
        created_at: new Date(Date.now() - 172800000).toISOString(), // 2 days ago
      },
      {
        id: "3",
        service_name: "GitHub",
        service_type: "Development",
        status: "inactive",
        created_at: new Date(Date.now() - 259200000).toISOString(), // 3 days ago
      }
    ];

    return NextResponse.json(mockConnections);
  } catch (error) {
    console.error('Error fetching connections:', error);
    return NextResponse.json({ error: 'Failed to fetch connections' }, { status: 500 });
  }
}

// done hadiqa