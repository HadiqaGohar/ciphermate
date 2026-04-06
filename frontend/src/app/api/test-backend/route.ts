import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:8000';

export async function GET() {
  try {
    // Test backend connection without authentication
    const response = await fetch(`${BACKEND_URL}/health`);
    const data = await response.json();
    
    return NextResponse.json({
      status: 'success',
      backend_status: data,
      message: 'Backend connection successful'
    });
  } catch (error) {
    return NextResponse.json({
      status: 'error',
      message: 'Failed to connect to backend',
      error: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Test chat endpoint without authentication
    const response = await fetch(`${BACKEND_URL}/api/v1/ai-agent/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    
    return NextResponse.json({
      status: response.ok ? 'success' : 'error',
      backend_response: data,
      status_code: response.status
    });
  } catch (error) {
    return NextResponse.json({
      status: 'error',
      message: 'Failed to test chat endpoint',
      error: error instanceof Error ? error.message : 'Unknown error'
    }, { status: 500 });
  }
}