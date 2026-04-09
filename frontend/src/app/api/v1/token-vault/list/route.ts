import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8080';

export async function GET(request: NextRequest) {
  try {
    // For hackathon demo: bypass auth and directly call backend
    const { searchParams } = new URL(request.url);
    const queryString = searchParams.toString();

    // Forward request to backend
    const response = await fetch(`${BACKEND_URL}/api/v1/token-vault/list?${queryString}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      // Return fallback data if backend fails
      return NextResponse.json({
        tokens: [
          {
            id: "demo_1",
            name: "Google Calendar",
            service: "google_calendar",
            service_name: "Google Calendar",
            status: "active",
            created_at: new Date().toISOString(),
            expires_at: new Date(Date.now() + 86400000 * 30).toISOString(),
            scopes: ["calendar.read", "calendar.write"],
            icon: "calendar",
            color: "#4285F4"
          },
          {
            id: "demo_2",
            name: "Gmail",
            service: "gmail",
            service_name: "Gmail",
            status: "active",
            created_at: new Date().toISOString(),
            expires_at: new Date(Date.now() + 86400000 * 25).toISOString(),
            scopes: ["email.read", "email.send"],
            icon: "mail",
            color: "#EA4335"
          }
        ],
        total: 2,
        summary: {
          total_tokens: 2,
          active_tokens: 2,
          expiring_soon: 0,
          expired: 0
        }
      });
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Error fetching token vault:', error);
    
    // Return fallback data on error
    return NextResponse.json({
      tokens: [
        {
          id: "demo_1",
          name: "Google Calendar",
          service: "google_calendar",
          service_name: "Google Calendar",
          status: "active",
          created_at: new Date().toISOString(),
          expires_at: new Date(Date.now() + 86400000 * 30).toISOString(),
          scopes: ["calendar.read", "calendar.write"],
          icon: "calendar",
          color: "#4285F4"
        }
      ],
      total: 1,
      summary: {
        total_tokens: 1,
        active_tokens: 1,
        expiring_soon: 0,
        expired: 0
      }
    });
  }
}