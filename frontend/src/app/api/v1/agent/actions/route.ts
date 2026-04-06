import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export async function GET(request: NextRequest) {
  try {
    // For hackathon demo: bypass auth and directly call backend
    const { searchParams } = new URL(request.url);
    const queryString = searchParams.toString();

    // Forward request to backend
    const response = await fetch(`${BACKEND_URL}/api/v1/agent/actions?${queryString}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      // Return fallback data if backend fails
      return NextResponse.json({
        actions: [
          {
            id: 1,
            name: "Create Calendar Event",
            description: "Create a new event in Google Calendar",
            service: "google_calendar",
            service_name: "Google Calendar",
            category: "calendar",
            parameters: [],
            permissions_required: ["calendar.write"],
            icon: "calendar",
            color: "#4285F4",
            status: "active"
          },
          {
            id: 2,
            name: "Send Email",
            description: "Send an email via Gmail",
            service: "gmail",
            service_name: "Gmail",
            category: "communication",
            parameters: [],
            permissions_required: ["email.send"],
            icon: "mail",
            color: "#EA4335",
            status: "active"
          }
        ],
        total: 2,
        categories: ["calendar", "communication"],
        services: ["google_calendar", "gmail"]
      });
    }

    const data = await response.json();
    return NextResponse.json(data);

  } catch (error) {
    console.error('Error fetching agent actions:', error);
    
    // Return fallback data on error
    return NextResponse.json({
      actions: [
        {
          id: 1,
          name: "Create Calendar Event",
          description: "Create a new event in Google Calendar",
          service: "google_calendar",
          service_name: "Google Calendar",
          category: "calendar",
          parameters: [],
          permissions_required: ["calendar.write"],
          icon: "calendar",
          color: "#4285F4",
          status: "active"
        }
      ],
      total: 1,
      categories: ["calendar"],
      services: ["google_calendar"]
    });
  }
}