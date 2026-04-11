import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Simulate creating a new action
    const newAction = {
      id: Date.now().toString(),
      agent_type: "demo",
      action: "Simulated AI task",
      status: "completed",
      created_at: new Date().toISOString(),
      result: { 
        success: true, 
        message: "Demo action completed successfully",
        processing_time: "2.3s"
      }
    };

    return NextResponse.json(newAction);
  } catch (error) {
    console.error('Error simulating action:', error);
    return NextResponse.json({ error: 'Failed to simulate action' }, { status: 500 });
  }
}
// done hadiqa
