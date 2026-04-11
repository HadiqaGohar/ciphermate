import { NextRequest, NextResponse } from "next/server";

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    if (!body.action_id) {
      return NextResponse.json(
        { error: "action_id is required" },
        { status: 400 }
      );
    }
// done hadiqa


    // Try to call the authenticated execute endpoint
    try {
      const authHeader = request.headers.get('Authorization');
      const backendResponse = await fetch(`${BACKEND_URL}/api/v1/agent/execute-action`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(authHeader && { 'Authorization': authHeader })
        },
        body: JSON.stringify({
          action_id: body.action_id,
          confirm: body.confirm || true
        }),
      });

      if (backendResponse.ok) {
        const backendResult = await backendResponse.json();
        
        return NextResponse.json({
          success: true,
          result: backendResult.result,
          status: backendResult.status,
          execution_time_ms: backendResult.execution_time_ms
        });
      } else if (backendResponse.status === 401) {
        return NextResponse.json({
          success: false,
          error: "Authentication required",
          message: "Please log in to execute actions",
          requires_auth: true
        }, { status: 401 });
      } else {
        throw new Error(`Backend responded with status: ${backendResponse.status}`);
      }
    } catch (backendError) {
      console.log('Backend not available or authentication failed:', backendError);
      
      return NextResponse.json({
        success: false,
        error: "Backend not available or authentication required",
        message: "Please ensure you are logged in and the backend is running"
      }, { status: 503 });
    }
  } catch (error) {
    console.error("Error executing action:", error);
    return NextResponse.json(
      {
        success: false,
        error: "Internal server error",
        message: "Failed to execute action. Please try again."
      },
      { status: 500 }
    );
  }
}