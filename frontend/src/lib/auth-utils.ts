/**
 * Authentication utilities for handling Auth0 tokens
 * Provides functions to extract, validate, and refresh Auth0 access tokens
 */

export interface AuthTokens {
  access_token: string;
  id_token: string;
  refresh_token?: string;
  expires_at?: number;
  token_type: "Bearer";
}

export interface UserSession {
  user: {
    sub: string;
    email: string;
    name: string;
    picture?: string;
  };
  accessToken: string;
  idToken: string;
  refreshToken?: string;
  timestamp: number;
}

export interface AuthError {
  error:
    | "AUTHENTICATION_ERROR"
    | "TOKEN_EXPIRED"
    | "TOKEN_INVALID"
    | "TOKEN_MISSING"
    | "TOKEN_REFRESH_FAILED"
    | "AUTH0_SERVICE_ERROR"
    | "NETWORK_ERROR"
    | "RATE_LIMIT_EXCEEDED"
    | "AUTHORIZATION_ERROR"
    | "TIMEOUT_ERROR"
    | "SERVICE_UNAVAILABLE"
    | "UNKNOWN_ERROR";
  message: string;
  details?: {
    reason: string;
    action: "login" | "refresh" | "retry";
  };
}

/**
 * Extract Auth0 access token from the current session
 * Uses the proper Auth0 NextJS SDK approach
 * @returns Promise<string | null> - Access token or null if not available
 */
export async function getAccessToken(): Promise<string | null> {
  try {
    // Use the Auth0 NextJS SDK's built-in getAccessToken function
    const response = await fetch("/api/auth/me", {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) {
      console.warn("Failed to get user session:", response.status);
      return null;
    }

    const sessionData = await response.json();

    if (!sessionData.authenticated) {
      return null;
    }

    // Get the session cookie and extract the access token
    const sessionCookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith("appSession="));

    if (!sessionCookie) {
      return null;
    }

    try {
      const sessionValue = decodeURIComponent(sessionCookie.split("=")[1]);
      const session: UserSession = JSON.parse(sessionValue);

      if (session.accessToken) {
        return session.accessToken;
      }
    } catch (parseError) {
      console.error("Error parsing session cookie:", parseError);
    }

    return null;
  } catch (error) {
    console.error("Error getting access token:", error);
    return null;
  }
}

/**
 * Validate if the current token is still valid
 * @param token - The access token to validate
 * @returns Promise<boolean> - True if token is valid
 */
export async function validateToken(token: string): Promise<boolean> {
  if (!token) {
    return false;
  }

  try {
    // Decode JWT token to check expiration
    const payload = token.split(".")[1];
    if (!payload) {
      return false;
    }

    const decoded = JSON.parse(atob(payload));
    const currentTime = Math.floor(Date.now() / 1000);

    // Check if token is expired (with 5 minute buffer)
    if (decoded.exp && decoded.exp < currentTime + 300) {
      return false;
    }

    return true;
  } catch (error) {
    console.error("Error validating token:", error);
    return false;
  }
}

/**
 * Attempt to refresh the access token using the refresh token
 * @returns Promise<string | null> - New access token or null if refresh failed
 */
export async function refreshAccessToken(): Promise<string | null> {
  try {
    // Get current session to extract refresh token
    const sessionCookie = document.cookie
      .split("; ")
      .find((row) => row.startsWith("appSession="));

    if (!sessionCookie) {
      throw new Error("No session found");
    }

    const sessionValue = decodeURIComponent(sessionCookie.split("=")[1]);
    const session: UserSession = JSON.parse(sessionValue);

    if (!session.refreshToken) {
      throw new Error("No refresh token available");
    }

    // Call Auth0 token endpoint to refresh
    const response = await fetch("/api/auth/refresh", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        refresh_token: session.refreshToken,
      }),
      credentials: "include",
    });

    if (!response.ok) {
      throw new Error(`Token refresh failed: ${response.status}`);
    }

    const data = await response.json();
    return data.access_token || null;
  } catch (error) {
    console.error("Error refreshing token:", error);
    return null;
  }
}

/**
 * Get a valid access token, refreshing if necessary
 * @returns Promise<string | null> - Valid access token or null if authentication failed
 */
export async function getValidAccessToken(): Promise<string | null> {
  try {
    // First, try to get the current token
    let token = await getAccessToken();

    if (!token) {
      return null;
    }

    // Validate the token
    const isValid = await validateToken(token);

    if (isValid) {
      return token;
    }

    // Token is invalid/expired, try to refresh
    console.log("Token expired, attempting refresh...");
    const refreshedToken = await refreshAccessToken();

    if (refreshedToken) {
      return refreshedToken;
    }

    // Refresh failed
    return null;
  } catch (error) {
    console.error("Error getting valid access token:", error);
    return null;
  }
}

/**
 * Handle authentication errors and provide appropriate actions
 * Enhanced with Auth0 service availability checking
 */
export function handleAuthError(error: any): AuthError {
  if (error?.status === 401) {
    return {
      error: "TOKEN_EXPIRED",
      message: "Your session has expired. Please log in again.",
      details: {
        reason: "Token expired or invalid",
        action: "login",
      },
    };
  }

  if (error?.status === 403) {
    return {
      error: "AUTHENTICATION_ERROR",
      message: "You do not have permission to perform this action.",
      details: {
        reason: "Insufficient permissions",
        action: "login",
      },
    };
  }

  if (
    error?.status === 503 ||
    error?.message?.includes("Service Unavailable")
  ) {
    return {
      error: "AUTH0_SERVICE_ERROR",
      message:
        "Authentication service is temporarily unavailable. Please try again in a few minutes.",
      details: {
        reason: "Auth0 service unavailable",
        action: "retry",
      },
    };
  }

  if (error?.status === 429) {
    return {
      error: "RATE_LIMIT_EXCEEDED",
      message:
        "Too many authentication attempts. Please wait before trying again.",
      details: {
        reason: "Rate limit exceeded",
        action: "retry",
      },
    };
  }

  if (
    error?.message?.includes("No session found") ||
    error?.message?.includes("No refresh token")
  ) {
    return {
      error: "TOKEN_MISSING",
      message: "Please log in to continue.",
      details: {
        reason: "No authentication session found",
        action: "login",
      },
    };
  }

  if (
    error?.message?.includes("Token refresh failed") ||
    error?.message?.includes("refresh")
  ) {
    return {
      error: "TOKEN_REFRESH_FAILED",
      message: "Unable to refresh your session. Please log in again.",
      details: {
        reason: "Token refresh failed",
        action: "login",
      },
    };
  }

  if (
    error?.message?.includes("fetch") ||
    error?.message?.includes("network")
  ) {
    return {
      error: "NETWORK_ERROR",
      message:
        "Network connection error. Please check your internet connection.",
      details: {
        reason: "Network connectivity issue",
        action: "retry",
      },
    };
  }

  return {
    error: "AUTHENTICATION_ERROR",
    message: "An authentication error occurred. Please try again.",
    details: {
      reason: error?.message || "Unknown authentication error",
      action: "retry",
    },
  };
}

/**
 * Check Auth0 service availability
 */
export async function checkAuth0ServiceAvailability(): Promise<boolean> {
  try {
    const auth0Domain =
      process.env.NEXT_PUBLIC_AUTH0_ISSUER_BASE_URL ||
      "https://dev-m40q4uji8sb8yhq0.us.auth0.com";

    // Try to reach Auth0's well-known configuration endpoint
    const response = await fetch(
      `${auth0Domain}/.well-known/openid_configuration`,
      {
        method: "GET",
        mode: "cors",
        cache: "no-cache",
      }
    );

    return response.ok;
  } catch (error) {
    console.error("Auth0 service availability check failed:", error);
    return false;
  }
}

/**
 * Enhanced token refresh with retry logic and service availability checking
 */
export async function refreshAccessTokenWithRetry(
  maxRetries: number = 3
): Promise<string | null> {
  let lastError: any = null;

  for (let attempt = 0; attempt < maxRetries; attempt++) {
    try {
      // Check Auth0 service availability before attempting refresh
      if (attempt > 0) {
        const isServiceAvailable = await checkAuth0ServiceAvailability();
        if (!isServiceAvailable) {
          console.warn(
            `Auth0 service unavailable on retry attempt ${attempt + 1}`
          );

          // Wait longer if service is unavailable
          const delay = Math.min(1000 * Math.pow(2, attempt), 10000); // Exponential backoff, max 10s
          await new Promise((resolve) => setTimeout(resolve, delay));
          continue;
        }
      }

      const token = await refreshAccessToken();
      if (token) {
        console.log(`✅ Token refresh successful on attempt ${attempt + 1}`);
        return token;
      }

      throw new Error("Token refresh returned null");
    } catch (error) {
      lastError = error;
      console.error(`Token refresh attempt ${attempt + 1} failed:`, error);

      // Don't retry on certain errors
      if (
        (error instanceof Error &&
          error.message?.includes("No session found")) ||
        (error instanceof Error &&
          error.message?.includes("No refresh token")) ||
        (error as any)?.status === 400
      ) {
        console.log("Non-retryable error, stopping retry attempts");
        break;
      }

      // Wait before retrying (exponential backoff)
      if (attempt < maxRetries - 1) {
        const delay = Math.min(1000 * Math.pow(2, attempt), 5000); // Max 5s delay
        console.log(`Waiting ${delay}ms before retry attempt ${attempt + 2}`);
        await new Promise((resolve) => setTimeout(resolve, delay));
      }
    }
  }

  console.error(`All ${maxRetries} token refresh attempts failed`);
  return null;
}

/**
 * Enhanced authentication recovery with automatic retry and graceful degradation
 */
export async function recoverFromAuthError(
  error: AuthError,
  maxRetries: number = 2
): Promise<string | null> {
  console.log("Starting authentication error recovery for:", error.error);

  switch (error.error) {
    case "TOKEN_EXPIRED":
    case "TOKEN_INVALID":
      // Try to refresh the token with retry logic
      console.log("Attempting token refresh for expired/invalid token...");
      const refreshedToken = await refreshAccessTokenWithRetry(maxRetries);

      if (refreshedToken) {
        console.log("✅ Authentication recovered via token refresh");
        return refreshedToken;
      }

      console.log(
        "Token refresh failed, redirecting to login with session clearing"
      );
      await forceLogoutAndRedirect();
      return null;

    case "TOKEN_REFRESH_FAILED":
      // Token refresh already failed, redirect to login
      console.log(
        "Token refresh previously failed, redirecting to login with session clearing"
      );
      await forceLogoutAndRedirect();
      return null;

    case "AUTH0_SERVICE_ERROR":
    case "NETWORK_ERROR":
      // Check service availability and retry if possible
      console.log("Checking Auth0 service availability...");
      const isServiceAvailable = await checkAuth0ServiceAvailability();

      if (isServiceAvailable) {
        console.log("Auth0 service is available, attempting token refresh...");
        const token = await refreshAccessTokenWithRetry(1); // Single retry for service errors

        if (token) {
          console.log("✅ Authentication recovered after service recovery");
          return token;
        }
      } else {
        console.log(
          "Auth0 service is unavailable, implementing graceful degradation"
        );

        // Implement graceful degradation - show offline mode or cached data
        await handleServiceUnavailability();
        return null;
      }

      // Show user-friendly error message but don't redirect immediately
      console.log("Service unavailable, showing error to user");
      return null;

    case "RATE_LIMIT_EXCEEDED":
      // Wait and retry once with exponential backoff
      console.log("Rate limit exceeded, implementing exponential backoff...");
      const backoffDelay = Math.min(5000 * Math.pow(2, maxRetries - 1), 30000); // Max 30s
      await new Promise((resolve) => setTimeout(resolve, backoffDelay));

      const retryToken = await refreshAccessToken();
      if (retryToken) {
        console.log("✅ Authentication recovered after rate limit wait");
        return retryToken;
      }

      console.log("Rate limit retry failed, redirecting to login");
      await forceLogoutAndRedirect();
      return null;

    case "TOKEN_MISSING":
    default:
      // No recovery possible, redirect to login
      console.log("No recovery possible for error type:", error.error);
      await forceLogoutAndRedirect();
      return null;
  }
}

/**
 * Handle Auth0 service unavailability with graceful degradation
 */
async function handleServiceUnavailability(): Promise<void> {
  console.log(
    "Implementing graceful degradation for Auth0 service unavailability"
  );

  // Store the current page for redirect after service recovery
  if (typeof window !== "undefined") {
    sessionStorage.setItem("auth_recovery_redirect", window.location.pathname);
  }

  // Show a user-friendly message instead of immediate redirect
  // This could be enhanced to show an offline mode or cached data
  const event = new CustomEvent("auth0ServiceUnavailable", {
    detail: {
      message:
        "Authentication service is temporarily unavailable. Some features may be limited.",
      action: "retry",
      retryAfter: 60000, // Suggest retry after 1 minute
    },
  });

  if (typeof window !== "undefined") {
    window.dispatchEvent(event);
  }
}

/**
 * Force logout with enhanced session clearing and redirect to login
 */
async function forceLogoutAndRedirect(): Promise<void> {
  try {
    console.log("Forcing logout with enhanced session clearing...");

    // Clear all local session data first
    clearLocalSession();

    // Clear any additional browser storage
    await clearAllAuthStorage();

    // Call logout endpoint to clear server-side session
    try {
      await fetch("/api/auth/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch (logoutError) {
      console.warn(
        "Server logout failed, but continuing with client-side cleanup:",
        logoutError
      );
    }

    // Force redirect to Auth0 logout with federated logout to clear all sessions
    const auth0Domain =
      process.env.NEXT_PUBLIC_AUTH0_ISSUER_BASE_URL ||
      "https://dev-m40q4uji8sb8yhq0.us.auth0.com";
    const clientId = process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID || "";
    const baseUrl =
      process.env.NEXT_PUBLIC_AUTH0_BASE_URL || window.location.origin;

    // Add federated=true to ensure social provider sessions are also cleared
    const logoutUrl =
      `${auth0Domain}/v2/logout?` +
      `client_id=${clientId}&` +
      `returnTo=${encodeURIComponent(baseUrl)}&` +
      `federated=true`; // This ensures Google/social provider sessions are cleared

    console.log("Redirecting to Auth0 logout with federated logout...");
    window.location.href = logoutUrl;
  } catch (error) {
    console.error("Force logout failed:", error);

    // Last resort - clear everything and redirect to home
    await clearAllAuthStorage();
    window.location.href = "/";
  }
}

/**
 * Clear all authentication-related storage (enhanced version)
 */
async function clearAllAuthStorage(): Promise<void> {
  try {
    // Clear cookies
    const cookiesToClear = [
      "appSession",
      "auth0",
      "auth0.is.authenticated",
      "_auth0",
      "auth0_compat",
      "a0_state",
    ];

    cookiesToClear.forEach((cookieName) => {
      // Clear for current domain
      document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;`;
      // Clear for parent domain
      document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=${window.location.hostname};`;
      // Clear for .domain
      const domain = window.location.hostname.split(".").slice(-2).join(".");
      document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.${domain};`;
    });

    // Clear localStorage
    if (typeof localStorage !== "undefined") {
      const keysToRemove = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (
          key &&
          (key.includes("auth") ||
            key.includes("token") ||
            key.includes("session") ||
            key.includes("a0_") ||
            key.includes("Auth0"))
        ) {
          keysToRemove.push(key);
        }
      }
      keysToRemove.forEach((key) => localStorage.removeItem(key));
    }

    // Clear sessionStorage
    if (typeof sessionStorage !== "undefined") {
      const keysToRemove = [];
      for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        if (
          key &&
          (key.includes("auth") ||
            key.includes("token") ||
            key.includes("session") ||
            key.includes("a0_") ||
            key.includes("Auth0"))
        ) {
          keysToRemove.push(key);
        }
      }
      keysToRemove.forEach((key) => sessionStorage.removeItem(key));
    }

    // Clear IndexedDB if it exists (some Auth0 implementations use it)
    if (typeof indexedDB !== "undefined") {
      try {
        const databases = await indexedDB.databases();
        for (const db of databases) {
          if (
            db.name &&
            (db.name.includes("auth") || db.name.includes("Auth0"))
          ) {
            indexedDB.deleteDatabase(db.name);
          }
        }
      } catch (idbError) {
        console.warn("Could not clear IndexedDB:", idbError);
      }
    }

    console.log("✅ All authentication storage cleared");
  } catch (error) {
    console.error("Error clearing authentication storage:", error);
  }
}

/**
 * Check if user is currently authenticated
 * @returns Promise<boolean> - True if user is authenticated
 */
export async function isAuthenticated(): Promise<boolean> {
  try {
    const response = await fetch("/api/auth/me", {
      method: "GET",
      credentials: "include",
    });

    if (!response.ok) {
      return false;
    }

    const data = await response.json();
    return data.authenticated === true;
  } catch (error) {
    console.error("Error checking authentication status:", error);
    return false;
  }
}

/**
 * Redirect user to login page
 */
export function redirectToLogin(): void {
  window.location.href = "/api/auth/login";
}

/**
 * Logout the current user with enhanced session clearing
 * This ensures users can login with different Gmail accounts after logout
 */
export async function logout(): Promise<void> {
  try {
    console.log("Starting enhanced logout process...");

    // Clear local session data first
    await clearAllAuthStorage();

    // Call logout endpoint to clear server-side session
    try {
      await fetch("/api/auth/logout", {
        method: "POST",
        credentials: "include",
      });
    } catch (logoutError) {
      console.warn(
        "Server logout failed, but continuing with Auth0 logout:",
        logoutError
      );
    }

    // Force redirect to Auth0 logout with federated logout to clear all sessions
    const auth0Domain =
      process.env.NEXT_PUBLIC_AUTH0_ISSUER_BASE_URL ||
      "https://dev-m40q4uji8sb8yhq0.us.auth0.com";
    const clientId = process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID || "";
    const baseUrl =
      process.env.NEXT_PUBLIC_AUTH0_BASE_URL || window.location.origin;

    // Add federated=true to ensure social provider sessions (Google, etc.) are also cleared
    // This allows users to login with different Gmail accounts
    const logoutUrl =
      `${auth0Domain}/v2/logout?` +
      `client_id=${clientId}&` +
      `returnTo=${encodeURIComponent(baseUrl)}&` +
      `federated=true`; // This is key for allowing different Gmail accounts

    console.log(
      "Redirecting to Auth0 logout with federated logout to clear all sessions..."
    );
    window.location.href = logoutUrl;
  } catch (error) {
    console.error("Error during logout:", error);

    // Clear local session even if logout request fails
    await clearAllAuthStorage();

    // Force redirect to Auth0 logout with federated logout
    try {
      const auth0Domain =
        process.env.NEXT_PUBLIC_AUTH0_ISSUER_BASE_URL ||
        "https://dev-m40q4uji8sb8yhq0.us.auth0.com";
      const clientId = process.env.NEXT_PUBLIC_AUTH0_CLIENT_ID || "";
      const baseUrl =
        process.env.NEXT_PUBLIC_AUTH0_BASE_URL || window.location.origin;

      const logoutUrl =
        `${auth0Domain}/v2/logout?` +
        `client_id=${clientId}&` +
        `returnTo=${encodeURIComponent(baseUrl)}&` +
        `federated=true`; // Ensure federated logout even in error case

      window.location.href = logoutUrl;
    } catch (fallbackError) {
      console.error("Fallback logout failed:", fallbackError);
      // Last resort - clear everything and redirect to home
      await clearAllAuthStorage();
      window.location.href = "/";
    }
  }
}

/**
 * Clear local session data to ensure clean logout (legacy function)
 * @deprecated Use clearAllAuthStorage() instead for enhanced clearing
 */
function clearLocalSession(): void {
  try {
    // Clear session cookie
    document.cookie =
      "appSession=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";

    // Clear any localStorage items related to auth
    if (typeof localStorage !== "undefined") {
      const keysToRemove = [];
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i);
        if (
          key &&
          (key.includes("auth") ||
            key.includes("token") ||
            key.includes("session"))
        ) {
          keysToRemove.push(key);
        }
      }
      keysToRemove.forEach((key) => localStorage.removeItem(key));
    }

    // Clear any sessionStorage items related to auth
    if (typeof sessionStorage !== "undefined") {
      const keysToRemove = [];
      for (let i = 0; i < sessionStorage.length; i++) {
        const key = sessionStorage.key(i);
        if (
          key &&
          (key.includes("auth") ||
            key.includes("token") ||
            key.includes("session"))
        ) {
          keysToRemove.push(key);
        }
      }
      keysToRemove.forEach((key) => sessionStorage.removeItem(key));
    }
  } catch (error) {
    console.error("Error clearing local session:", error);
  }
}
