import { NextResponse } from 'next/server';

interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
  environment: string;
  uptime: number;
  backend?: {
    status: string;
    statusCode?: number;
    error?: string;
  };
}

export async function GET() {
  try {
    // Basic health check
    const health: HealthResponse = {
      status: 'healthy',
      timestamp: new Date().toISOString(),
      version: process.env.NEXT_PUBLIC_APP_VERSION || '1.0.0',
      environment: process.env.NEXT_PUBLIC_ENVIRONMENT || 'development',
      uptime: process.uptime(),
    };

    // Check if backend is reachable (optional)
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL;
    if (backendUrl) {
      try {
        const response = await fetch(`${backendUrl}/health`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
          // Short timeout for health check
          signal: AbortSignal.timeout(5000),
        });
        
        health.backend = {
          status: response.ok ? 'healthy' : 'unhealthy',
          statusCode: response.status,
        };
      } catch (error) {
        health.backend = {
          status: 'unreachable',
          error: error instanceof Error ? error.message : 'Unknown error',
        };
      }
    }

    return NextResponse.json(health, { status: 200 });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}