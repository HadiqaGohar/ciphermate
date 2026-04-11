import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export async function middleware(request: NextRequest) {
  console.log('Middleware running for:', request.nextUrl.pathname);
  
  // For now, let's just allow everything to pass through
  // This will get your app running without the infinite redirect
  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
// done hadiqa
