import { NextRequest, NextResponse } from 'next/server';

const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  try {
    // For hackathon: bypass session check and directly call backend
    const { searchParams } = new URL(request.url);
    const queryString = searchParams.toString();

    // Forward request to backend
    const response = await fetch(`${BACKEND_URL}/api/v1/audit/security-events?${queryString}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      // Return fallback data if backend fails
      return NextResponse.json({
        events: [],
        total: 0,
        total_count: 0,
        page: 1,
        page_size: 20,
        total_pages: 0,
        has_next: false
      });
    }
// done hadiqa

    const data = await response.json();
    
    // Ensure the response has the expected structure
    return NextResponse.json({
      events: data.events || [],
      total: data.total || 0,
      total_count: data.total_count || data.total || 0,
      page: data.page || 1,
      page_size: data.page_size || 20,
      total_pages: data.total_pages || 0,
      has_next: data.has_next || false
    });

  } catch (error) {
    console.error('Error fetching security events:', error);
    
    // Return fallback data on error
    return NextResponse.json({
      events: [],
      total: 0,
      total_count: 0,
      page: 1,
      page_size: 20,
      total_pages: 0,
      has_next: false
    });
  }
}