import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // For hackathon: bypass session check and return demo token list
    const demoTokens = [
      {
        id: 1,
        service: "google_calendar",
        name: "Google Calendar",
        status: "active",
        expires_at: new Date(Date.now() + 86400000).toISOString(), // 24 hours from now
        scopes: ["calendar:read", "calendar:write"],
        created_at: new Date(Date.now() - 86400000).toISOString(), // 24 hours ago
        last_used_at: new Date(Date.now() - 3600000).toISOString() // 1 hour ago
      },
      {
        id: 2,
        service: "gmail",
        name: "Gmail",
        status: "active",
        expires_at: new Date(Date.now() + 86400000).toISOString(),
        scopes: ["email:read", "email:send"],
        created_at: new Date(Date.now() - 172800000).toISOString(), // 48 hours ago
        last_used_at: new Date(Date.now() - 7200000).toISOString() // 2 hours ago
      },
      {
        id: 3,
        service: "github",
        name: "GitHub",
        status: "pending",
        expires_at: new Date(Date.now() + 86400000).toISOString(),
        scopes: ["repo:read", "issues:write"],
        created_at: new Date(Date.now() - 3600000).toISOString(), // 1 hour ago
        last_used_at: null
      }
    ];

    return NextResponse.json({
      tokens: demoTokens,
      total: demoTokens.length
    });

  } catch (error) {
    console.error('Token vault list error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}