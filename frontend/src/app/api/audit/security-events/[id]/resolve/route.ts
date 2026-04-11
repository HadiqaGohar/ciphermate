import { NextRequest, NextResponse } from 'next/server';

export async function POST(
  request: NextRequest,
  { params }: { params: Promise<{ id: string }> }
) {
  try {
    const { id: eventId } = await params;
    
    // For hackathon: simulate resolving the event
    console.log(`Resolving security event ${eventId}`);
    
    // In a real implementation, this would update the database
    // For now, just return success
    return NextResponse.json({
      success: true,
      message: `Security event ${eventId} has been resolved`,
      resolved_at: new Date().toISOString()
    });

  } catch (error) {
    console.error('Error resolving security event:', error);
    return NextResponse.json(
      { error: 'Failed to resolve security event' },
      { status: 500 }
    );
  }
}
// done hadiqa
