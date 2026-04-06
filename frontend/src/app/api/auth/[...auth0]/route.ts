// Auth0 route handler for Next.js App Router
import { NextRequest } from "next/server";

export async function GET(request: NextRequest) {
  return new Response("Auth0 handler - GET method", { status: 200 });
}

export async function POST(request: NextRequest) {
  return new Response("Auth0 handler - POST method", { status: 200 });
}
