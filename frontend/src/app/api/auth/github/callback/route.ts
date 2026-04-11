import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const code = searchParams.get('code');
  const error = searchParams.get('error');
  const state = searchParams.get('state');

  // If there's an error, show it directly
  if (error) {
    const html = `
      <!DOCTYPE html>
      <html>
      <head><title>GitHub OAuth Failed</title></head>
      <body style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
        <h2 style="color: red;">❌ GitHub Authorization Failed</h2>
        <p>Error: ${error}</p>
        <script>
          if (window.opener) {
            window.opener.postMessage({ type: 'oauth_error', service: 'github', error: '${error}' }, '*');
          }
          setTimeout(() => window.close(), 2000);
        </script>
      </body>
      </html>
    `;
    return new NextResponse(html, {
      headers: { 'Content-Type': 'text/html' },
      status: 400,
    });
  }

  // Redirect to backend to handle the OAuth callback and store tokens
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
  const callbackUrl = `${backendUrl}/api/auth/github/callback?code=${code}&state=${state}`;

  return NextResponse.redirect(callbackUrl, 302);
}