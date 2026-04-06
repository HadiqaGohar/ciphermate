import { NextRequest, NextResponse } from 'next/server';

export async function DELETE(
  request: NextRequest,
  { params }: { params: Promise<{ service: string }> }
) {
  try {
    // For hackathon: bypass session check and return demo response
    const { service } = await params;

    return NextResponse.json({
      success: true,
      message: `Token for ${service} has been revoked`,
      service,
      revoked_at: new Date().toISOString()
    });

  } catch (error) {
    console.error('Token vault revoke error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}