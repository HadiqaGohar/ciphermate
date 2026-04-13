import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const searchParams = request.nextUrl.searchParams;
  const code = searchParams.get("code");
  const error = searchParams.get("error");
  const state = searchParams.get("state");

  console.log("📥 Gmail OAuth Callback received:", { code: code?.substring(0, 20), error, state });

  // Handle error from Google
  if (error) {
    console.error("❌ Gmail OAuth Error:", error);
    return sendResponse(`
      <div class="error">
        <h2>❌ Authorization Failed</h2>
        <p>Error: ${error}</p>
        <p>Please try again or contact support.</p>
        <button onclick="window.close()">Close Window</button>
      </div>
    `, false);
  }

  // No code received
  if (!code) {
    console.error("❌ No authorization code received");
    return sendResponse(`
      <div class="error">
        <h2>❌ Authorization Failed</h2>
        <p>No authorization code received.</p>
        <button onclick="window.close()">Close Window</button>
      </div>
    `, false);
  }

  try {
    // Exchange code for tokens using backend
    const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8080";
    
    // Use production URL for Vercel deployment, localhost for local development
    const frontendUrl = process.env.NODE_ENV === 'production' 
      ? 'https://ciphermate.vercel.app' 
      : 'http://localhost:3000';

    const response = await fetch(`${backendUrl}/api/v1/auth/gmail/callback`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        code: code,
        redirect_uri: `${frontendUrl}/api/v1/auth/gmail/callback`
      }),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to exchange token");
    }

    const tokenData = await response.json();
    console.log("✅ Token exchange successful");

    // Send success response
    return sendResponse(`
      <div class="success">
        <h2>✅ Gmail Connected Successfully!</h2>
        <p>🎉 Your Gmail has been connected to CipherMate.</p>
        <p>You can now send emails via the chat interface.</p>
        <p><small>This window will close automatically in 3 seconds...</small></p>
      </div>
    `, true, tokenData);

  } catch (error: any) {
    console.error("❌ Token exchange error:", error);
    return sendResponse(`
      <div class="error">
        <h2>❌ Connection Failed</h2>
        <p>Failed to connect Gmail: ${error.message}</p>
        <p>Please try again.</p>
        <button onclick="window.close()">Close Window</button>
      </div>
    `, false);
  }
}

function sendResponse(content: string, success: boolean, tokenData?: any) {
  const html = `
    <!DOCTYPE html>
    <html>
    <head>
      <title>Gmail OAuth - CipherMate</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
          text-align: center;
          padding: 50px 20px;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          min-height: 100vh;
          display: flex;
          justify-content: center;
          align-items: center;
        }
        .container {
          background: white;
          padding: 40px;
          border-radius: 20px;
          box-shadow: 0 20px 60px rgba(0,0,0,0.3);
          max-width: 500px;
          margin: 0 auto;
        }
        .success {
          color: #10b981;
          font-size: 48px;
          margin-bottom: 20px;
        }
        .error {
          color: #ef4444;
          font-size: 48px;
          margin-bottom: 20px;
        }
        h2 {
          color: #1f2937;
          margin-bottom: 15px;
          font-size: 24px;
        }
        p {
          color: #6b7280;
          margin-bottom: 20px;
          line-height: 1.5;
        }
        button {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          border: none;
          padding: 12px 24px;
          border-radius: 8px;
          font-size: 16px;
          cursor: pointer;
          margin-top: 20px;
        }
        button:hover {
          transform: translateY(-2px);
          box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="${success ? 'success' : 'error'}">
          ${success ? '✓' : '✗'}
        </div>
        ${content}
      </div>
      <script>
        // Send message to parent window
        if (window.opener && !window.opener.closed) {
          try {
            window.opener.postMessage({
              type: '${success ? 'oauth_success' : 'oauth_error'}',
              service: 'gmail',
              success: ${success},
              ${success ? `token_data: ${JSON.stringify(tokenData || {})}` : ''}
            }, '*');
            console.log('📤 Sent message to parent window');
          } catch(e) {
            console.error('Failed to send message:', e);
          }
        }

        // Auto-close on success after 3 seconds
        ${success ? `
          setTimeout(() => {
            window.close();
          }, 3000);
        ` : ''}
      </script>
    </body>
    </html>
  `;

  return new NextResponse(html, {
    headers: {
      "Content-Type": "text/html",
    },
  });
}