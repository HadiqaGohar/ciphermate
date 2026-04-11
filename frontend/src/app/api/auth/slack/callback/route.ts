import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const code = searchParams.get('code');
  const error = searchParams.get('error');
  const state = searchParams.get('state');

  // Create a simple HTML page that sends a message to the parent window
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Slack OAuth Callback</title>
    </head>
    <body>
      <div style="text-align: center; padding: 50px; font-family: Arial, sans-serif;">
        ${error ? 
          `<h2 style="color: red;">❌ Slack Authorization Failed</h2>
           <p>Error: ${error}</p>` :
          `<h2 style="color: green;">✅ Slack Authorization Successful</h2>
           <p>You can close this window now.</p>`
        }
      </div>
      <script>
        // Send message to parent window
        if (window.opener) {
          window.opener.postMessage({
            type: '${error ? 'oauth_error' : 'oauth_success'}',
            service: 'slack',
            code: '${code || ''}',
            error: '${error || ''}',
            state: '${state || ''}'
          }, '*');
        }
        
        // Auto-close after 2 seconds
        setTimeout(() => {
          window.close();
        }, 2000);
      </script>
    </body>
    </html>
  `;

  return new NextResponse(html, {
    headers: {
      'Content-Type': 'text/html',
    },
  });
}