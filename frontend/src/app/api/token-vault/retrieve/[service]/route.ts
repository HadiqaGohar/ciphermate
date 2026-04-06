import { NextRequest, NextResponse } from 'next/server';

export async function GET(
  request: NextRequest,
  { params }: { params: Promise<{ service: string }> }
) {
  try {
    // For hackathon: bypass session check and return demo response
    const { service } = await params;

    // Return demo token data
    return NextResponse.json({
      service,
      token: "demo_token_" + service,
      expires_at: new Date(Date.now() + 3600000).toISOString(), // 1 hour from now
      scopes: ["read", "write"],
      status: "active"
    });

  } catch (error) {
    console.error('Token vault retrieve error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}