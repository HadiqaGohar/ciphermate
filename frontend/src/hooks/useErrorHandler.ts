'use client';

import { useCallback, useState, useRef } from 'react';
import { useRouter } from 'next/navigation';
import { 
  AuthErrorHandler, 
  EnhancedAuthError, 
  ErrorContext, 
  RetryConfig,
  createAuthErrorHandler,
  isAuthenticationError,
  isRetryableError,
  formatErrorForDisplay
} from '../lib/error-handling';
import { redirectToLogin } from '../lib/auth-utils';

export interface ErrorState {
  error: EnhancedAuthError | null;
  isError: boolean;
  isRetrying: boolean;
  retryCount: number;
  canRetry: boolean;
  nextRetryAt: Date | null;
}

export interface ErrorHandlerOptions {
  showToast?: boolean;
  logError?: boolean;
  redirectOnAuth?: boolean;
  retryable?: boolean;
  maxRetries?: number;
  retryConfig?: Partial<RetryConfig>;
  onLogin?: () => void;
  onRefresh?: () => Promise<void>;
  onContactSupport?: () => void;
}

export function useErrorHandler(options: ErrorHandlerOptions = {}) {
  const {
    showToast = true,
    logError = true,
    redirectOnAuth = true,
    retryable = true,
    maxRetries = 3,
    retryConfig,
    onLogin,
    onRefresh,
    onContactSupport
  } = options;

  const router = useRouter();
  const errorHandlerRef = useRef<AuthErrorHandler | null>(null);
  
  const [errorState, setErrorState] = useState<ErrorState>({
    error: null,
    isError: false,
    isRetrying: false,
    retryCount: 0,
    canRetry: false,
    nextRetryAt: null
  });

  // Initialize error handler
  if (!errorHandlerRef.current) {
    errorHandlerRef.current = createAuthErrorHandler(
      retryConfig,
      {
        onLogin: onLogin || (() => redirectToLogin()),
        onRefresh,
        onContactSupport: onContactSupport || (() => {
          window.open('mailto:support@ciphermate.com?subject=Authentication Error');
        })
      }
    );
  }

  const logErrorToService = useCallback((error: EnhancedAuthError, context?: ErrorContext) => {
    if (!logError || !errorHandlerRef.current) return;
    
    errorHandlerRef.current.logError(error);
  }, [logError]);

  const showErrorToast = useCallback((error: EnhancedAuthError) => {
    if (!showToast) return;

    const displayInfo = formatErrorForDisplay(error);
    
    // In a real app, you'd use a toast library like react-hot-toast
    // For now, we'll use console.warn (replace with proper toast implementation)
    console.warn(`${displayInfo.title}: ${displayInfo.message}`);
    
    // Example with react-hot-toast:
    // toast.error(`${displayInfo.title}: ${displayInfo.message}`, {
    //   duration: 5000,
    //   position: 'top-right'
    // });
  }, [showToast]);

  const handleError = useCallback(async (
    error: any,
    context: ErrorContext = {},
    customHandler?: (error: EnhancedAuthError) => void | Promise<void>
  ): Promise<EnhancedAuthError> => {
    if (!errorHandlerRef.current) {
      throw new Error('Error handler not initialized');
    }

    // Process the error with enhanced information
    const enhancedError = errorHandlerRef.current.processError(error, context);
    
    // Update error state
    setErrorState({
      error: enhancedError,
      isError: true,
      isRetrying: false,
      retryCount: enhancedError.retryCount || 0,
      canRetry: enhancedError.isRetryable || false,
      nextRetryAt: enhancedError.nextRetryAt || null
    });

    // Log error for monitoring
    logErrorToService(enhancedError, context);

    // Handle specific authentication errors
    if (isAuthenticationError(enhancedError) && redirectOnAuth) {
      await handleAuthenticationError(enhancedError);
    }

    // Show user notification
    showErrorToast(enhancedError);

    // Call custom handler if provided
    if (customHandler) {
      await customHandler(enhancedError);
    }

    return enhancedError;
  }, [logErrorToService, showErrorToast, redirectOnAuth]);

  const handleAuthenticationError = useCallback(async (error: EnhancedAuthError) => {
    switch (error.error) {
      case 'TOKEN_EXPIRED':
      case 'TOKEN_INVALID':
        // Try to refresh token first, then redirect to login if that fails
        if (onRefresh) {
          try {
            await onRefresh();
            clearError(); // Clear error if refresh succeeds
            return;
          } catch (refreshError) {
            console.error('Token refresh failed:', refreshError);
          }
        }
        // Fall through to login redirect
        
      case 'TOKEN_MISSING':
      case 'AUTHENTICATION_ERROR':
        if (redirectOnAuth) {
          console.log('Redirecting to login due to authentication error');
          redirectToLogin();
        }
        break;

      case 'AUTHORIZATION_ERROR':
        // Don't automatically redirect for authorization errors
        // User might need to request additional permissions
        break;

      default:
        // Handle other auth errors as needed
        break;
    }
  }, [onRefresh, redirectOnAuth]);

  const retry = useCallback(async <T>(
    retryFn: () => Promise<T>,
    context: ErrorContext = {}
  ): Promise<T | null> => {
    if (!retryable || !errorHandlerRef.current) {
      console.warn('Retry not enabled or error handler not available');
      return null;
    }

    const currentError = errorState.error;
    if (!currentError || !currentError.isRetryable) {
      console.warn('Current error is not retryable');
      return null;
    }

    setErrorState(prev => ({ ...prev, isRetrying: true }));

    try {
      // Use the error handler's retry logic with exponential backoff
      const result = await errorHandlerRef.current!.withRetry(
        retryFn,
        { ...context, operation: context.operation || 'manual_retry' },
        { maxAttempts: maxRetries }
      );
      
      // Clear error on successful retry
      clearError();
      return result;
      
    } catch (retryError) {
      // Handle retry failure
      const enhancedRetryError = errorHandlerRef.current!.processError(retryError, context);
      
      setErrorState(prev => ({
        ...prev,
        error: enhancedRetryError,
        isRetrying: false,
        retryCount: enhancedRetryError.retryCount || prev.retryCount + 1,
        canRetry: (enhancedRetryError.isRetryable && (enhancedRetryError.retryCount || 0) < maxRetries) || false,
        nextRetryAt: enhancedRetryError.nextRetryAt || null
      }));

      // Log the retry failure
      logErrorToService(enhancedRetryError, context);
      
      return null;
    }
  }, [retryable, errorState.error, maxRetries, logErrorToService]);

  const retryWithDelay = useCallback(async <T>(
    retryFn: () => Promise<T>,
    context: ErrorContext = {}
  ): Promise<T | null> => {
    if (!errorHandlerRef.current || !errorState.error) {
      return null;
    }

    const delay = errorHandlerRef.current.calculateRetryDelay(errorState.retryCount);
    
    setErrorState(prev => ({
      ...prev,
      nextRetryAt: new Date(Date.now() + delay)
    }));

    // Wait for the calculated delay
    await new Promise(resolve => setTimeout(resolve, delay));
    
    return retry(retryFn, context);
  }, [retry, errorState.error, errorState.retryCount]);

  const clearError = useCallback(() => {
    setErrorState({
      error: null,
      isError: false,
      isRetrying: false,
      retryCount: 0,
      canRetry: false,
      nextRetryAt: null
    });
  }, []);

  const getErrorMessage = useCallback((error?: EnhancedAuthError) => {
    const currentError = error || errorState.error;
    if (!currentError || !errorHandlerRef.current) return '';

    return errorHandlerRef.current.getUserFriendlyMessage(currentError);
  }, [errorState.error]);

  const getErrorDisplay = useCallback((error?: EnhancedAuthError) => {
    const currentError = error || errorState.error;
    if (!currentError) return null;

    return formatErrorForDisplay(currentError);
  }, [errorState.error]);

  const getRecoveryActions = useCallback((error?: EnhancedAuthError) => {
    const currentError = error || errorState.error;
    if (!currentError?.recoveryActions) return [];

    // Update action handlers with current context
    return currentError.recoveryActions.map(action => ({
      ...action,
      action: () => {
        switch (action.type) {
          case 'retry':
            if (retryable && currentError.isRetryable) {
              // This would need to be connected to the original operation
              console.log('Retry action triggered');
            }
            break;
          case 'dismiss':
            clearError();
            break;
          default:
            // Call the original action
            action.action();
            break;
        }
      }
    }));
  }, [errorState.error, retryable, clearError]);

  const isAuthError = useCallback((error?: EnhancedAuthError) => {
    const currentError = error || errorState.error;
    return currentError ? isAuthenticationError(currentError) : false;
  }, [errorState.error]);

  const canRetryError = useCallback((error?: EnhancedAuthError) => {
    const currentError = error || errorState.error;
    if (!currentError) return false;
    
    return isRetryableError(currentError) && 
           (currentError.retryCount || 0) < maxRetries;
  }, [errorState.error, maxRetries]);

  return {
    // State
    ...errorState,
    
    // Actions
    handleError,
    clearError,
    retry,
    retryWithDelay,
    
    // Getters
    getErrorMessage,
    getErrorDisplay,
    getRecoveryActions,
    
    // Utilities
    isAuthError,
    canRetryError
  };
}

// Utility function for handling fetch errors with enhanced error processing
export async function handleFetchError(response: Response): Promise<never> {
  let errorData: any;

  try {
    errorData = await response.json();
  } catch {
    errorData = {
      error: 'HTTP_ERROR',
      message: response.statusText || 'Request failed',
      status: response.status,
      timestamp: new Date().toISOString()
    };
  }

  // Create an error object that includes the response
  const error = new Error(errorData.message || 'Request failed');
  (error as any).response = response;
  (error as any).status = response.status;
  (error as any).data = errorData;

  throw error;
}

// Enhanced fetch wrapper with comprehensive error handling and retry logic
export async function apiRequest<T = any>(
  url: string,
  options: RequestInit = {},
  retryConfig?: Partial<RetryConfig>
): Promise<T> {
  const errorHandler = createAuthErrorHandler(retryConfig);
  
  const operation = async (): Promise<T> => {
    const response = await fetch(url, {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    });

    if (!response.ok) {
      await handleFetchError(response);
    }

    return response.json();
  };

  return errorHandler.withRetry(operation, {
    operation: 'api_request',
    url,
    method: options.method || 'GET'
  });
}