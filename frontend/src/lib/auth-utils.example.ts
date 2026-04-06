/**
 * Example usage of auth utilities
 * This file demonstrates how to use the authentication utilities
 */

import {
  getValidAccessToken,
  isAuthenticated,
  handleAuthError,
  redirectToLogin,
  logout
} from './auth-utils';

/**
 * Example: Making an authenticated API request
 */
export async function makeAuthenticatedRequest(url: string, options: RequestInit = {}) {
  try {
    // Check if user is authenticated first
    const authenticated = await isAuthenticated();
    if (!authenticated) {
      redirectToLogin();
      return null;
    }

    // Get a valid access token (will refresh if needed)
    const token = await getValidAccessToken();
    if (!token) {
      // Token couldn't be obtained or refreshed
      redirectToLogin();
      return null;
    }

    // Make the request with the token
    const response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      // Handle authentication errors
      if (response.status === 401 || response.status === 403) {
        const authError = handleAuthError({ status: response.status });
        console.error('Authentication error:', authError);
        
        if (authError.details?.action === 'login') {
          redirectToLogin();
        }
        return null;
      }
      
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    return response;
  } catch (error) {
    const authError = handleAuthError(error);
    console.error('Request failed:', authError);
    
    if (authError.details?.action === 'login') {
      redirectToLogin();
    }
    
    throw error;
  }
}

/**
 * Example: Chat API request using auth utilities
 */
export async function sendChatMessage(message: string) {
  try {
    const response = await makeAuthenticatedRequest('/api/chat', {
      method: 'POST',
      body: JSON.stringify({ message }),
    });

    if (!response) {
      throw new Error('Authentication failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Chat request failed:', error);
    throw error;
  }
}

/**
 * Example: Component-level authentication check
 */
export async function checkAuthenticationStatus() {
  try {
    const authenticated = await isAuthenticated();
    
    if (!authenticated) {
      return {
        authenticated: false,
        action: 'login' as const,
        message: 'Please log in to continue'
      };
    }

    const token = await getValidAccessToken();
    
    if (!token) {
      return {
        authenticated: false,
        action: 'login' as const,
        message: 'Session expired, please log in again'
      };
    }

    return {
      authenticated: true,
      token,
      message: 'Authentication successful'
    };
  } catch (error) {
    const authError = handleAuthError(error);
    return {
      authenticated: false,
      action: authError.details?.action || 'retry' as const,
      message: authError.message
    };
  }
}

/**
 * Example: Logout with error handling
 */
export async function handleLogout() {
  try {
    await logout();
  } catch (error) {
    console.error('Logout failed:', error);
    // Force redirect even if logout fails
    window.location.href = '/';
  }
}