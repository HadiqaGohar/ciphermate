import { NextRequest, NextResponse } from "next/server";

// Auth0 configuration
const AUTH0_DOMAIN = process.env.AUTH0_ISSUER_BASE_URL || "https://dev-m40q4uji8sb8yhq0.us.auth0.com";
const AUTH0_CLIENT_ID = process.env.AUTH0_CLIENT_ID || "";
const AUTH0_CLIENT_SECRET = process.env.AUTH0_CLIENT_SECRET || "";
const BASE_URL = process.env.AUTH0_BASE_URL || "http://localhost:3000";

/**
 * Auth0 Dynamic Route Handler
 * Handles: /api/auth/login, /api/auth/logout, /api/auth/callback, /api/auth/me
 */
export async function GET(request: NextRequest) {
  const { pathname } = new URL(request.url);
  const segments = pathname.split("/");
  const action = segments[segments.length - 1];

  try {
    switch (action) {
      case "login":
        return handleLogin();
      
      case "logout":
        return handleLogout();
      
      case "callback":
        return handleCallback(request);
      
      case "me":
        return handleGetUser(request);
      
      default:
        return NextResponse.json(
          { error: "Invalid auth action", action },
          { status: 400 }
        );
    }
  } catch (error) {
    console.error("Auth error:", error);
    return NextResponse.json(
      {
        error: "Authentication error",
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  const { pathname } = new URL(request.url);
  const segments = pathname.split("/");
  const action = segments[segments.length - 1];

  try {
    switch (action) {
      case "logout":
        return handleLogout();
      
      case "refresh":
        return handleRefreshToken(request);
      
      default:
        return GET(request);
    }
  } catch (error) {
    console.error("Auth POST error:", error);
    return NextResponse.json(
      {
        error: "Authentication error",
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}

/**
 * Redirect to Auth0 login page with enhanced session clearing
 * Forces fresh login to ensure different accounts can be used
 */
function handleLogin(): NextResponse {
  const loginUrl = `${AUTH0_DOMAIN}/authorize?` + 
    `response_type=code&` +
    `client_id=${AUTH0_CLIENT_ID}&` +
    `redirect_uri=${encodeURIComponent(BASE_URL + "/api/auth/callback")}&` +
    `scope=openid profile email offline_access&` +
    `prompt=login`; // Force fresh login to ensure different accounts can be used

  const response = NextResponse.redirect(loginUrl);
  
  // Clear any existing session cookies before redirecting to login
  response.cookies.delete("appSession");
  response.cookies.delete("auth0");
  response.cookies.delete("auth0.is.authenticated");
  response.cookies.delete("_auth0");
  response.cookies.delete("auth0_compat");
  response.cookies.delete("a0_state");
  
  // Set headers to prevent caching
  response.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate');
  response.headers.set('Pragma', 'no-cache');
  response.headers.set('Expires', '0');
  
  return response;
}

/**
 * Logout and clear session with enhanced Auth0 session clearing
 * Includes federated logout to clear social provider sessions (Google, etc.)
 */
function handleLogout(): NextResponse {
  const logoutUrl = `${AUTH0_DOMAIN}/v2/logout?` +
    `client_id=${AUTH0_CLIENT_ID}&` +
    `returnTo=${encodeURIComponent(BASE_URL)}&` +
    `federated=true`; // Add federated logout to clear social provider sessions

  const response = NextResponse.redirect(logoutUrl);
  
  // Clear all possible session cookies
  response.cookies.delete("appSession");
  
  // Clear any other Auth0 related cookies
  response.cookies.delete("auth0");
  response.cookies.delete("auth0.is.authenticated");
  response.cookies.delete("_auth0");
  response.cookies.delete("auth0_compat");
  response.cookies.delete("a0_state");
  
  // Set additional headers to prevent caching and ensure clean logout
  response.headers.set('Cache-Control', 'no-cache, no-store, must-revalidate');
  response.headers.set('Pragma', 'no-cache');
  response.headers.set('Expires', '0');
  response.headers.set('Clear-Site-Data', '"cache", "cookies", "storage"'); // Modern browsers
  
  return response;
}

/**
 * Handle Auth0 callback - exchange code for tokens
 */
async function handleCallback(request: NextRequest): Promise<NextResponse> {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");
  const error = searchParams.get("error");
  const state = searchParams.get("state");

  // Handle Auth0 error
  if (error) {
    console.error("Auth0 error:", error);
    return NextResponse.redirect(`${BASE_URL}/auth/login?error=${error}`);
  }

  if (!code) {
    console.error("No authorization code received");
    return NextResponse.redirect(`${BASE_URL}/auth/login?error=no_code`);
  }

  try {
    // Exchange authorization code for tokens
    const tokenResponse = await fetch(`${AUTH0_DOMAIN}/oauth/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        grant_type: "authorization_code",
        client_id: AUTH0_CLIENT_ID,
        client_secret: AUTH0_CLIENT_SECRET,
        code,
        redirect_uri: `${BASE_URL}/api/auth/callback`,
      }),
    });

    if (!tokenResponse.ok) {
      const errorData = await tokenResponse.json().catch(() => ({}));
      console.error("Token exchange failed:", errorData);
      return NextResponse.redirect(`${BASE_URL}/auth/login?error=token_exchange_failed`);
    }

    const tokens = await tokenResponse.json();
    const { id_token, access_token, refresh_token } = tokens;

    // Decode ID token to get user info
    let user = null;
    if (id_token) {
      try {
        const payload = id_token.split('.')[1];
        const decoded = JSON.parse(atob(payload));
        user = {
          name: decoded.name,
          email: decoded.email,
          picture: decoded.picture,
          sub: decoded.sub,
        };
      } catch (decodeError) {
        console.error("Error decoding ID token:", decodeError);
      }
    }

    // Create session
    const sessionData = {
      accessToken: access_token,
      idToken: id_token,
      refreshToken: refresh_token,
      user,
      timestamp: Date.now(),
    };

    // Create response with redirect to dashboard
    const response = NextResponse.redirect(`${BASE_URL}/dashboard`);

    // Set session cookie
    response.cookies.set("appSession", JSON.stringify(sessionData), {
      httpOnly: true,
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
      maxAge: 60 * 60 * 24 * 7, // 7 days
      path: "/",
    });

    console.log("✅ User logged in:", user?.email);
    return response;

  } catch (error) {
    console.error("Callback error:", error);
    return NextResponse.redirect(`${BASE_URL}/auth/login?error=callback_error`);
  }
}

/**
 * Handle token refresh using refresh token
 */
async function handleRefreshToken(request: NextRequest): Promise<NextResponse> {
  try {
    const body = await request.json();
    const { refresh_token } = body;

    if (!refresh_token) {
      return NextResponse.json(
        { error: "Refresh token is required" },
        { status: 400 }
      );
    }

    // Exchange refresh token for new access token
    const tokenResponse = await fetch(`${AUTH0_DOMAIN}/oauth/token`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        grant_type: "refresh_token",
        client_id: AUTH0_CLIENT_ID,
        client_secret: AUTH0_CLIENT_SECRET,
        refresh_token,
      }),
    });

    if (!tokenResponse.ok) {
      const errorData = await tokenResponse.json().catch(() => ({}));
      console.error("Token refresh failed:", errorData);
      return NextResponse.json(
        { error: "Token refresh failed", details: errorData },
        { status: tokenResponse.status }
      );
    }

    const tokens = await tokenResponse.json();
    const { access_token, id_token } = tokens;

    // Get current session to update it
    const sessionCookie = request.cookies.get("appSession");
    if (sessionCookie) {
      try {
        const currentSession = JSON.parse(sessionCookie.value);
        
        // Update session with new tokens
        const updatedSession = {
          ...currentSession,
          accessToken: access_token,
          idToken: id_token,
          timestamp: Date.now(),
        };

        const response = NextResponse.json({
          access_token,
          token_type: "Bearer",
          success: true,
        });

        // Update session cookie
        response.cookies.set("appSession", JSON.stringify(updatedSession), {
          httpOnly: true,
          secure: process.env.NODE_ENV === "production",
          sameSite: "lax",
          maxAge: 60 * 60 * 24 * 7, // 7 days
          path: "/",
        });

        return response;
      } catch (parseError) {
        console.error("Error parsing session during refresh:", parseError);
      }
    }

    // If no session cookie, just return the new token
    return NextResponse.json({
      access_token,
      token_type: "Bearer",
      success: true,
    });

  } catch (error) {
    console.error("Refresh token error:", error);
    return NextResponse.json(
      {
        error: "Token refresh failed",
        details: error instanceof Error ? error.message : "Unknown error",
      },
      { status: 500 }
    );
  }
}

/**
 * Get current user from session
 */
function handleGetUser(request: NextRequest): NextResponse {
  const sessionCookie = request.cookies.get("appSession");

  if (!sessionCookie) {
    return NextResponse.json({ user: null, authenticated: false });
  }

  try {
    const session = JSON.parse(sessionCookie.value);
    
    // Check if session is expired
    const sessionAge = Date.now() - session.timestamp;
    const maxAge = 7 * 24 * 60 * 60 * 1000; // 7 days in ms

    if (sessionAge > maxAge) {
      const response = NextResponse.json({ user: null, authenticated: false });
      response.cookies.delete("appSession");
      return response;
    }

    return NextResponse.json({
      user: session.user,
      authenticated: true,
      email: session.user?.email,
    });
  } catch (error) {
    console.error("Error parsing session:", error);
    const response = NextResponse.json({ user: null, authenticated: false });
    response.cookies.delete("appSession");
    return response;
  }
}
