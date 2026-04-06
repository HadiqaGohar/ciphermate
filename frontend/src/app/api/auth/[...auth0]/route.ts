// Auth0 route handler for Next.js App Router
export async function GET() {
  return new Response('Auth0 handler - GET method', { status: 200 });
}

export async function POST() {
  return new Response('Auth0 handler - POST method', { status: 200 });
}
