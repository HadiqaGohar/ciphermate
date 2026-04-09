import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // For now, return mock data since DISABLE_AGENTS=true
    const mockActions = [
      {
        id: "1",
        agent_type: "email",
        action: "Send welcome email",
        status: "completed",
        created_at: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
        result: { success: true, message: "Email sent successfully" }
      },
      {
        id: "2",
        agent_type: "github", 
        action: "Create repository backup",
        status: "completed",
        created_at: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
        result: { success: true, backup_url: "https://github.com/backup/repo" }
      }
    ];

    return NextResponse.json(mockActions);
  } catch (error) {
    console.error('Error fetching actions:', error);
    return NextResponse.json({ error: 'Failed to fetch actions' }, { status: 500 });
  }
}