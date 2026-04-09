import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const mockStats = {
      total_users: 1,
      total_connections: 2,
      total_actions: 5,
      total_tokens: 1250,
      uptime: "99.9%",
      api_calls_today: 47,
      active_agents: 3
    };

    return NextResponse.json(mockStats);
  } catch (error) {
    console.error('Error fetching stats:', error);
    return NextResponse.json({ error: 'Failed to fetch stats' }, { status: 500 });
  }
}