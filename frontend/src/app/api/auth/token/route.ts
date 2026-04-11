import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // For hackathon: return mock token
    return NextResponse.json({
      accessToken: 'mock-access-token-for-hackathon',
      user: {
        sub: 'mock-user-123',
        email: 'test@example.com',
        name: 'Test User'
      }
    });

  } catch (error) {
    console.error('Error getting access token:', error);
    return NextResponse.json(
      { error: 'Failed to get access token' },
      { status: 500 }
    );
  }
}
// done hadiqa
