'use client';

import { useCallback, useEffect, useState } from 'react';
import { 
  getValidAccessToken, 
  isAuthenticated, 
  handleAuthError, 
  redirectToLogin, 
  logout,
  type AuthError 
} from '../lib/auth-utils';

export interface AuthState {
  user: any;
  isLoading: boolean;
  isAuthenticated: boolean;
  error: AuthError | null;
  accessToken: string | null;
  isTokenValid: boolean;
  isRefreshing: boolean;
  tokenExpiresAt: number | null;
}

export interface AuthActions {
  getAccessToken: () => Promise<string | null>;
  refreshToken: () => Promise<string | null>;
  login: () => void;
  logout: () => Promise<void>;
  clearError: () => void;
  isTokenExpiringSoon: () => boolean;
}

export interface UseAuthReturn extends AuthState, AuthActions {}

/**
 * Custom authentication hook that provides comprehensive Auth0 integration
 * with token management, refresh capabilities, and error handling
 * 
 * This version uses custom session management instead of Auth0's useUser hook
 * to avoid React context conflicts with React 19
 */
export function useAuth(): UseAuthReturn {
  const [authState, setAuthState] = useState<{
    user: any;
    accessToken: string | null;
    isTokenValid: boolean;
    isRefreshing: boolean;
    error: AuthError | null;
    isAuthenticated: boolean;
    tokenExpiresAt: number | null;
    isLoading: boolean;
  }>({
    user: null,
    accessToken: null,
    isTokenValid: false,
    isRefreshing: false,
    error: null,
    isAuthenticated: false,
    tokenExpiresAt: null,
    isLoading: true,
  });

  // Initialize authentication state from session cookie
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // Check if user is authenticated by checking session cookie
        const authenticated = await isAuthenticated();
        
        if (authenticated) {
          // Get user info from session cookie
          const sessionCookie = document.cookie
            .split('; ')
            .find(row => row.startsWith('appSession='));
          
          let user: any = null;
          let accessToken: string | null = null;
          let expiresAt: number | null = null;
          
          if (sessionCookie) {
            try {
              const sessionValue = decodeURIComponent(sessionCookie.split('=')[1]);
              const session = JSON.parse(sessionValue);
              user = session.user;
              accessToken = session.accessToken;
              
              // Extract expiration time from token
              if (accessToken) {
                try {
                  const payload = accessToken.split('.')[1];
                  if (payload) {
                    const decoded = JSON.parse(atob(payload));
                    expiresAt = decoded.exp ? decoded.exp * 1000 : null;
                  }
                } catch (decodeError) {
                  console.error('Error decoding token for expiration:', decodeError);
                }
              }
            } catch (parseError) {
              console.error('Error parsing session cookie:', parseError);
            }
          }
          
          setAuthState(prev => ({
            ...prev,
            user,
            accessToken,
            isTokenValid: !!accessToken,
            isAuthenticated: true,
            tokenExpiresAt: expiresAt,
            isLoading: false,
          }));
        } else {
          setAuthState(prev => ({
            ...prev,
            user: null,
            accessToken: null,
            isTokenValid: false,
            isAuthenticated: false,
            tokenExpiresAt: null,
            isLoading: false,
          }));
        }
      } catch (error) {
        const authError = handleAuthError(error);
        setAuthState(prev => ({
          ...prev,
          error: authError,
          isAuthenticated: false,
          isLoading: false,
        }));
      }
    };

    initializeAuth();
  }, []);

  // Set up token expiration monitoring
  useEffect(() => {
    let tokenCheckInterval: NodeJS.Timeout;

    if (authState.isAuthenticated && authState.accessToken) {
      // Check token validity every 5 minutes
      tokenCheckInterval = setInterval(async () => {
        try {
          const token = authState.accessToken;
          if (token) {
            // Decode JWT to check expiration
            const payload = token.split('.')[1];
            if (payload) {
              const decoded = JSON.parse(atob(payload));
              const currentTime = Math.floor(Date.now() / 1000);
              
              // If token expires in less than 10 minutes, refresh it
              if (decoded.exp && decoded.exp < (currentTime + 600)) {
                console.log('Token expiring soon, refreshing...');
                // Call refresh directly to avoid circular dependency
                try {
                  setAuthState(prev => ({ ...prev, isRefreshing: true, error: null }));

                  // Get current session to extract refresh token
                  const sessionCookie = document.cookie
                    .split('; ')
                    .find(row => row.startsWith('appSession='));

                  if (!sessionCookie) {
                    throw new Error('No session found for token refresh');
                  }

                  const sessionValue = decodeURIComponent(sessionCookie.split('=')[1]);
                  const session = JSON.parse(sessionValue);

                  if (!session.refreshToken) {
                    throw new Error('No refresh token available');
                  }

                  // Call the refresh endpoint
                  const response = await fetch('/api/auth/refresh', {
                    method: 'POST',
                    headers: {
                      'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                      refresh_token: session.refreshToken,
                    }),
                    credentials: 'include',
                  });

                  if (!response.ok) {
                    const errorData = await response.json().catch(() => ({}));
                    throw new Error(`Token refresh failed: ${errorData.error || response.statusText}`);
                  }

                  const data = await response.json();
                  const newToken = data.access_token;

                  if (!newToken) {
                    throw new Error('No access token received from refresh');
                  }

                  // Extract expiration time from new token
                  let expiresAt: number | null = null;
                  try {
                    const payload = newToken.split('.')[1];
                    if (payload) {
                      const decoded = JSON.parse(atob(payload));
                      expiresAt = decoded.exp ? decoded.exp * 1000 : null;
                    }
                  } catch (decodeError) {
                    console.error('Error decoding refreshed token for expiration:', decodeError);
                  }

                  setAuthState(prev => ({
                    ...prev,
                    accessToken: newToken,
                    isTokenValid: true,
                    isRefreshing: false,
                    error: null,
                    tokenExpiresAt: expiresAt,
                  }));

                  console.log('✅ Token refreshed successfully');
                } catch (error) {
                  console.error('Automatic token refresh failed:', error);
                  const authError = handleAuthError(error);
                  
                  setAuthState(prev => ({
                    ...prev,
                    error: authError,
                    isRefreshing: false,
                    isTokenValid: false,
                    accessToken: null,
                  }));

                  // If refresh fails, redirect to login
                  if (authError.details?.action === 'login') {
                    console.log('Automatic refresh failed, redirecting to login...');
                    redirectToLogin();
                  }
                }
              }
            }
          }
        } catch (error) {
          console.error('Error checking token expiration:', error);
        }
      }, 5 * 60 * 1000); // Check every 5 minutes
    }

    return () => {
      if (tokenCheckInterval) {
        clearInterval(tokenCheckInterval);
      }
    };
  }, [authState.isAuthenticated, authState.accessToken]);

  /**
   * Get access token, refreshing if necessary with enhanced error recovery
   */
  const getAccessToken = useCallback(async (): Promise<string | null> => {
    try {
      setAuthState(prev => ({ ...prev, isRefreshing: true, error: null }));

      const token = await getValidAccessToken();
      let expiresAt = null;
      
      // Extract expiration time from token
      if (token) {
        try {
          const payload = token.split('.')[1];
          if (payload) {
            const decoded = JSON.parse(atob(payload));
            expiresAt = decoded.exp ? decoded.exp * 1000 : null;
          }
        } catch (decodeError) {
          console.error('Error decoding token for expiration:', decodeError);
        }
      }
      
      setAuthState(prev => ({
        ...prev,
        accessToken: token,
        isTokenValid: !!token,
        isRefreshing: false,
        tokenExpiresAt: expiresAt,
      }));

      return token;
    } catch (error) {
      const authError = handleAuthError(error);
      
      // Try enhanced recovery for certain error types
      if (authError.error === 'TOKEN_EXPIRED' || authError.error === 'TOKEN_INVALID') {
        console.log('Token expired/invalid, attempting enhanced recovery...');
        
        try {
          // Import recovery function dynamically to avoid circular dependency
          const { recoverFromAuthError } = await import('../lib/auth-utils');
          const recoveredToken = await recoverFromAuthError(authError, 3);
          
          if (recoveredToken) {
            // Extract expiration time from recovered token
            let expiresAt: number | null = null;
            try {
              const payload = recoveredToken.split('.')[1];
              if (payload) {
                const decoded = JSON.parse(atob(payload));
                expiresAt = decoded.exp ? decoded.exp * 1000 : null;
              }
            } catch (decodeError) {
              console.error('Error decoding recovered token for expiration:', decodeError);
            }
            
            setAuthState(prev => ({
              ...prev,
              accessToken: recoveredToken,
              isTokenValid: true,
              isRefreshing: false,
              error: null,
              tokenExpiresAt: expiresAt,
            }));
            
            console.log('✅ Token recovered successfully in useAuth');
            return recoveredToken;
          }
        } catch (recoveryError) {
          console.error('Enhanced recovery failed:', recoveryError);
        }
      }
      
      setAuthState(prev => ({
        ...prev,
        error: authError,
        isRefreshing: false,
        isTokenValid: false,
        accessToken: null,
      }));
      
      return null;
    }
  }, []);

  /**
   * Force refresh the access token
   */
  const refreshToken = useCallback(async (): Promise<string | null> => {
    try {
      setAuthState(prev => ({ ...prev, isRefreshing: true, error: null }));

      // Get current session to extract refresh token
      const sessionCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('appSession='));

      if (!sessionCookie) {
        throw new Error('No session found for token refresh');
      }

      const sessionValue = decodeURIComponent(sessionCookie.split('=')[1]);
      const session = JSON.parse(sessionValue);

      if (!session.refreshToken) {
        throw new Error('No refresh token available');
      }

      // Call the refresh endpoint
      const response = await fetch('/api/auth/refresh', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          refresh_token: session.refreshToken,
        }),
        credentials: 'include',
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`Token refresh failed: ${errorData.error || response.statusText}`);
      }

      const data = await response.json();
      const newToken = data.access_token;

      if (!newToken) {
        throw new Error('No access token received from refresh');
      }

      // Extract expiration time from new token
      let expiresAt = null;
      try {
        const payload = newToken.split('.')[1];
        if (payload) {
          const decoded = JSON.parse(atob(payload));
          expiresAt = decoded.exp ? decoded.exp * 1000 : null;
        }
      } catch (decodeError) {
        console.error('Error decoding refreshed token for expiration:', decodeError);
      }

      setAuthState(prev => ({
        ...prev,
        accessToken: newToken,
        isTokenValid: true,
        isRefreshing: false,
        error: null,
        tokenExpiresAt: expiresAt,
      }));

      console.log('✅ Token refreshed successfully');
      return newToken;

    } catch (error) {
      console.error('Token refresh failed:', error);
      const authError = handleAuthError(error);
      
      setAuthState(prev => ({
        ...prev,
        error: authError,
        isRefreshing: false,
        isTokenValid: false,
        accessToken: null,
      }));

      // If refresh fails, redirect to login
      if (authError.details?.action === 'login') {
        console.log('Refresh failed, redirecting to login...');
        redirectToLogin();
      }

      return null;
    }
  }, []);

  /**
   * Redirect to login page
   */
  const login = useCallback(() => {
    redirectToLogin();
  }, []);

  /**
   * Logout the current user with enhanced session clearing
   */
  const handleLogout = useCallback(async (): Promise<void> => {
    try {
      await logout();
      setAuthState({
        user: null,
        accessToken: null,
        isTokenValid: false,
        isRefreshing: false,
        error: null,
        isAuthenticated: false,
        tokenExpiresAt: null,
        isLoading: false,
      });
    } catch (error) {
      const authError = handleAuthError(error);
      setAuthState(prev => ({
        ...prev,
        error: authError,
      }));
      
      // Even if logout fails, clear local state and redirect
      console.log('Logout error, but clearing local state and redirecting anyway');
      setAuthState({
        user: null,
        accessToken: null,
        isTokenValid: false,
        isRefreshing: false,
        error: null,
        isAuthenticated: false,
        tokenExpiresAt: null,
        isLoading: false,
      });
    }
  }, []);

  /**
   * Clear any authentication errors
   */
  const clearError = useCallback(() => {
    setAuthState(prev => ({
      ...prev,
      error: null,
    }));
  }, []);

  /**
   * Check if the current token is expiring soon (within 10 minutes)
   */
  const isTokenExpiringSoon = useCallback((): boolean => {
    if (!authState.tokenExpiresAt) {
      return false;
    }
    
    const currentTime = Date.now();
    const timeUntilExpiry = authState.tokenExpiresAt - currentTime;
    const tenMinutesInMs = 10 * 60 * 1000;
    
    return timeUntilExpiry <= tenMinutesInMs;
  }, [authState.tokenExpiresAt]);

  return {
    // State
    user: authState.user,
    isLoading: authState.isLoading,
    isAuthenticated: authState.isAuthenticated && !!authState.user,
    error: authState.error,
    accessToken: authState.accessToken,
    isTokenValid: authState.isTokenValid,
    isRefreshing: authState.isRefreshing,
    tokenExpiresAt: authState.tokenExpiresAt,
    
    // Actions
    getAccessToken,
    refreshToken,
    login,
    logout: handleLogout,
    clearError,
    isTokenExpiringSoon,
  };
}
