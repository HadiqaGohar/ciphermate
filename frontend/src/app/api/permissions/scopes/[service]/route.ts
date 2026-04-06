import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ service: string }> }
) {
  try {
    // For hackathon: bypass session check and return demo scopes
    const { service } = await params;

    // Return demo scopes for each service
    const scopes: Record<string, string[]> = {
      google_calendar: [
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/calendar.events'
      ],
      gmail: [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send'
      ],
      github: [
        'repo',
        'user:email',
        'read:org'
      ],
      slack: [
        'channels:read',
        'chat:write',
        'groups:read'
      ]
    };

    const serviceScopes = scopes[service] || [];
    
    return NextResponse.json({
      service,
      scopes: serviceScopes,
      required: serviceScopes,
      optional: []
    });

  } catch (error) {
    console.error('Service scopes error:', error);
    return NextResponse.json(
      { error: 'Failed to load service scopes' },
      { status: 500 }
    );
  }
}