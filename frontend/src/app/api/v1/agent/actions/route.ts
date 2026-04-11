import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Return mock agent actions in the format the dashboard expects
    const mockAgentActions = [
      {
        id: 1,
        action_type: "EMAIL_SEND",
        service_name: "gmail",
        status: "completed",
        created_at: new Date(Date.now() - 10 * 60 * 1000).toISOString(), // 10 min ago
        executed_at: new Date(Date.now() - 9 * 60 * 1000).toISOString(),
        result: "Email sent successfully to team@example.com",
        parameters: { 
          to: "team@example.com", 
          subject: "Project Update",
          body: "Here's the latest project status..." 
        }
      },
      {
        id: 2,
        action_type: "CALENDAR_CREATE_EVENT",
        service_name: "google_calendar",
        status: "completed",
        created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(), // 2 hours ago
        executed_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString(),
        result: "Event 'Team Meeting' created successfully",
        parameters: { 
          title: "Team Meeting",
          date: "2026-04-10",
          time: "14:00"
        }
      },
      {
        id: 3,
        action_type: "GITHUB_CREATE_ISSUE",
        service_name: "github",
        status: "completed",
        created_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(), // 1 day ago
        executed_at: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000).toISOString(),
        result: "Issue #42 created: Fix login bug",
        parameters: { 
          title: "Fix login bug",
          repo: "ciphermate/app"
        }
      },
      {
        id: 4,
        action_type: "SLACK_SEND_MESSAGE",
        service_name: "slack",
        status: "pending",
        created_at: new Date(Date.now() - 5 * 60 * 1000).toISOString(), // 5 min ago
        parameters: { 
          channel: "#general", 
          text: "Team standup in 5 minutes!" 
        }
      },
      {
        id: 5,
        action_type: "EMAIL_SEND",
        service_name: "gmail",
        status: "completed",
        created_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(), // 3 days ago
        executed_at: new Date(Date.now() - 3 * 24 * 60 * 60 * 1000).toISOString(),
        result: "Welcome email sent to new user",
        parameters: { 
          to: "newuser@example.com", 
          subject: "Welcome to CipherMate!"
        }
      }
    ];

    return NextResponse.json(mockAgentActions);
  } catch (error) {
    console.error('Error fetching agent actions:', error);
    return NextResponse.json({ error: 'Failed to fetch agent actions' }, { status: 500 });
  }
}