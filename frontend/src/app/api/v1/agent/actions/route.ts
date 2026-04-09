import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Return mock agent actions in the format the dashboard expects
    const mockAgentActions = [
      {
        id: "1",
        agent_type: "email",
        action: "Send automated welcome email",
        status: "completed",
        created_at: new Date(Date.now() - 1800000).toISOString(), // 30 min ago
        result: "Email sent successfully to 5 recipients"
      },
      {
        id: "2", 
        agent_type: "github",
        action: "Create repository backup",
        status: "completed",
        created_at: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
        result: "Repository backed up to cloud storage"
      },
      {
        id: "3",
        agent_type: "slack",
        action: "Post daily standup reminder",
        status: "pending",
        created_at: new Date().toISOString(),
        result: null
      },
      {
        id: "4",
        agent_type: "task",
        action: "Generate weekly report",
        status: "completed",
        created_at: new Date(Date.now() - 7200000).toISOString(), // 2 hours ago
        result: "Report generated and shared with team"
      }
    ];

    return NextResponse.json(mockAgentActions);
  } catch (error) {
    console.error('Error fetching agent actions:', error);
    return NextResponse.json({ error: 'Failed to fetch agent actions' }, { status: 500 });
  }
}