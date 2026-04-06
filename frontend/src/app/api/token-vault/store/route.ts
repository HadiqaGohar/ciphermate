import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // For hackathon: bypass session check and return demo response
    const body = await request.json();
    const { service, token, scopes } = body;

    return NextResponse.json({
      success: true,
      message: `Token for ${service} has been stored`,
      service,
      scopes: scopes || ["read", "write"],
      stored_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + 86400000).toISOString() // 24 hours from now
    });

  } catch (error) {
    console.error('Token vault store error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}