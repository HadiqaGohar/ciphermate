/**
 * Comprehensive error handling utilities for authentication failures
 * Provides user-friendly error messages and automatic retry logic for transient failures
 */

import { AuthError } from './auth-utils';

export interface ErrorContext {
  operation?: string;
  url?: string;
  method?: string;
  timestamp?: string;
  userAgent?: string;
  requestId?: string;
}

export interface RetryConfig {
  maxAttempts: number;
  baseDelay: number;
  maxDelay: number;
  backoffMultiplier: number;
  retryableErrors: string[];
}

export interface ErrorRecoveryAction {
  type: 'login' | 'refresh' | 'retry' | 'wait' | 'contact_support' | 'dismiss';
  label: string;
  description?: string;
  action: () => void | Promise<void>;
  primary: boolean;
  disabled?: boolean;
  countdown?: number;
}

export interface EnhancedAuthError extends AuthError {
  context?: ErrorContext;
  recoveryActions?: ErrorRecoveryAction[];
  isRetryable?: boolean;
  retryCount?: number;
  nextRetryAt?: Date;
  userFriendlyMessage?: string;
  technicalDetails?: string;
}

/**
 * Default retry configuration for different types of errors
 */
export const DEFAULT_RETRY_CONFIG: RetryConfig = {
  maxAttempts: 3,
  baseDelay: 1000, // 1 second
  maxDelay: 30000, // 30 seconds
  backoffMultiplier: 2,
  retryableErrors: [
    'NETWORK_ERROR',
    'TIMEOUT_ERROR',
    'SERVICE_UNAVAILABLE',
    'RATE_LIMIT_EXCEEDED',
    'TOKEN_REFRESH_FAILED'
  ]
};

/**
 * User-friendly error messages for different authentication failure scenarios
 */
export const ERROR_MESSAGES: Record<string, { title: string; message: string; suggestion: string }> = {
  TOKEN_EXPIRED: {
    title: 'Session Expired',
    message: 'Your session has expired for security reasons.',
    suggestion: 'Please log in again to continue using the application.'
  },
  TOKEN_INVALID: {
    title: 'Authentication Error',
    message: 'There was a problem with your authentication.',
    suggestion: 'Please log in again to verify your identity.'
  },
  TOKEN_MISSING: {
    title: 'Not Logged In',
    message: 'You need to be logged in to access this feature.',
    suggestion: 'Please log in to continue.'
  },
  TOKEN_REFRESH_FAILED: {
    title: 'Session Refresh Failed',
    message: 'We couldn\'t refresh your session automatically.',
    suggestion: 'Please log in again to continue.'
  },
  AUTHENTICATION_ERROR: {
    title: 'Authentication Failed',
    message: 'We couldn\'t verify your identity.',
    suggestion: 'Please check your credentials and try logging in again.'
  },
  AUTHORIZATION_ERROR: {
    title: 'Access Denied',
    message: 'You don\'t have permission to perform this action.',
    suggestion: 'Contact your administrator if you believe this is an error.'
  },
  NETWORK_ERROR: {
    title: 'Connection Problem',
    message: 'We\'re having trouble connecting to our servers.',
    suggestion: 'Please check your internet connection and try again.'
  },
  TIMEOUT_ERROR: {
    title: 'Request Timeout',
    message: 'The request took too long to complete.',
    suggestion: 'Please try again. If the problem persists, check your connection.'
  },
  SERVICE_UNAVAILABLE: {
    title: 'Service Temporarily Unavailable',
    message: 'Our authentication service is temporarily unavailable.',
    suggestion: 'Please try again in a few minutes.'
  },
  RATE_LIMIT_EXCEEDED: {
    title: 'Too Many Attempts',
    message: 'You\'ve made too many requests in a short time.',
    suggestion: 'Please wait a moment before trying again.'
  },
  AUTH0_SERVICE_ERROR: {
    title: 'Authentication Service Error',
    message: 'There\'s a problem with our authentication provider.',
    suggestion: 'Please try again later or contact support if the issue persists.'
  },
  CORS_ERROR: {
    title: 'Browser Security Error',
    message: 'Your browser blocked the request for security reasons.',
    suggestion: 'Please refresh the page and try again.'
  },
  UNKNOWN_ERROR: {
    title: 'Unexpected Error',
    message: 'Something unexpected happened.',
    suggestion: 'Please try again or contact support if the problem continues.'
  }
};

/**
 * Enhanced error handler class for authentication failures
 */
export class AuthErrorHandler {
  private retryConfig: RetryConfig;
  private onLogin?: () => void;
  private onRefresh?: () => Promise<void>;
  private onContactSupport?: () => void;

  constructor(
    config: Partial<RetryConfig> = {},
    callbacks: {
      onLogin?: () => void;
      onRefresh?: () => Promise<void>;
      onContactSupport?: () => void;
    } = {}
  ) {
    this.retryConfig = { ...DEFAULT_RETRY_CONFIG, ...config };
    this.onLogin = callbacks.onLogin;
    this.onRefresh = callbacks.onRefresh;
    this.onContactSupport = callbacks.onContactSupport;
  }

  /**
   * Process and enhance an authentication error with user-friendly information
   */
  processError(
    error: AuthError | Error | any,
    context: ErrorContext = {}
  ): EnhancedAuthError {
    const enhancedError = this.normalizeError(error);
    
    // Add context information
    enhancedError.context = {
      timestamp: new Date().toISOString(),
      userAgent: typeof window !== 'undefined' ? window.navigator.userAgent : undefined,
      ...context
    };

    // Add user-friendly message
    const errorInfo = ERROR_MESSAGES[enhancedError.error] || ERROR_MESSAGES.UNKNOWN_ERROR;
    enhancedError.userFriendlyMessage = errorInfo.message;
    enhancedError.technicalDetails = enhancedError.message;

    // Determine if error is retryable
    enhancedError.isRetryable = this.isRetryableError(enhancedError.error);

    // Generate recovery actions
    enhancedError.recoveryActions = this.generateRecoveryActions(enhancedError);

    return enhancedError;
  }

  /**
   * Normalize different error types into a consistent format
   */
  private normalizeError(error: any): EnhancedAuthError {
    // If it's already an AuthError, use it as base
    if (error && typeof error === 'object' && error.error) {
      return { ...error };
    }

    // Handle fetch/network errors
    if (error instanceof TypeError && error.message.includes('fetch')) {
      return {
        error: 'NETWORK_ERROR',
        message: 'Network request failed',
        details: {
          reason: error.message,
          action: 'retry' as const
        }
      };
    }

    // Handle timeout errors
    if (error?.name === 'AbortError' || error?.message?.includes('timeout')) {
      return {
        error: 'TIMEOUT_ERROR',
        message: 'Request timed out',
        details: {
          reason: 'Request took too long to complete',
          action: 'retry' as const
        }
      };
    }

    // Handle HTTP status errors
    if (error?.status || error?.response?.status) {
      const status = error.status || error.response.status;
      
      switch (status) {
        case 401:
          return {
            error: 'TOKEN_EXPIRED',
            message: 'Authentication required',
            details: {
              reason: 'Token expired or invalid',
              action: 'login' as const
            }
          };
        case 403:
          return {
            error: 'AUTHORIZATION_ERROR',
            message: 'Access forbidden',
            details: {
              reason: 'Insufficient permissions',
              action: 'login' as const
            }
          };
        case 429:
          return {
            error: 'RATE_LIMIT_EXCEEDED',
            message: 'Too many requests',
            details: {
              reason: 'Rate limit exceeded',
              action: 'retry' as const
            }
          };
        case 503:
          return {
            error: 'SERVICE_UNAVAILABLE',
            message: 'Service temporarily unavailable',
            details: {
              reason: 'Server is temporarily unavailable',
              action: 'retry' as const
            }
          };
        default:
          return {
            error: 'AUTHENTICATION_ERROR',
            message: `HTTP ${status} error`,
            details: {
              reason: error.message || 'Unknown HTTP error',
              action: 'retry' as const
            }
          };
      }
    }

    // Handle generic errors
    if (error instanceof Error) {
      return {
        error: 'UNKNOWN_ERROR',
        message: error.message,
        details: {
          reason: error.message,
          action: 'retry' as const
        }
      };
    }

    // Handle string errors
    if (typeof error === 'string') {
      return {
        error: 'UNKNOWN_ERROR',
        message: error,
        details: {
          reason: error,
          action: 'retry' as const
        }
      };
    }

    // Fallback for unknown error types
    return {
      error: 'UNKNOWN_ERROR',
      message: 'An unknown error occurred',
      details: {
        reason: 'Unknown error type',
        action: 'retry' as const
      }
    };
  }

  /**
   * Check if an error type is retryable
   */
  private isRetryableError(errorType: string): boolean {
    return this.retryConfig.retryableErrors.includes(errorType);
  }

  /**
   * Generate recovery actions based on error type
   */
  private generateRecoveryActions(error: EnhancedAuthError): ErrorRecoveryAction[] {
    const actions: ErrorRecoveryAction[] = [];
    const errorInfo = ERROR_MESSAGES[error.error] || ERROR_MESSAGES.UNKNOWN_ERROR;

    switch (error.error) {
      case 'TOKEN_EXPIRED':
      case 'TOKEN_INVALID':
      case 'TOKEN_MISSING':
      case 'AUTHENTICATION_ERROR':
        actions.push({
          type: 'login',
          label: 'Log In Again',
          description: errorInfo.suggestion,
          action: () => this.onLogin?.(),
          primary: true
        });
        break;

      case 'TOKEN_REFRESH_FAILED':
        if (this.onRefresh) {
          actions.push({
            type: 'refresh',
            label: 'Refresh Session',
            description: 'Try to refresh your authentication session',
            action: () => this.onRefresh?.(),
            primary: true
          });
        }
        actions.push({
          type: 'login',
          label: 'Log In Again',
          description: 'Start a fresh session',
          action: () => this.onLogin?.(),
          primary: false
        });
        break;

      case 'NETWORK_ERROR':
      case 'TIMEOUT_ERROR':
      case 'SERVICE_UNAVAILABLE':
        if (error.isRetryable) {
          actions.push({
            type: 'retry',
            label: 'Try Again',
            description: errorInfo.suggestion,
            action: () => {}, // Will be set by retry handler
            primary: true
          });
        }
        break;

      case 'RATE_LIMIT_EXCEEDED':
        const retryAfter = this.calculateRetryDelay(error.retryCount || 0);
        actions.push({
          type: 'wait',
          label: `Wait ${Math.ceil(retryAfter / 1000)}s`,
          description: 'Wait before trying again',
          action: () => {}, // Will be set by retry handler
          primary: true,
          countdown: retryAfter
        });
        break;

      case 'AUTHORIZATION_ERROR':
        actions.push({
          type: 'login',
          label: 'Check Permissions',
          description: 'Log in with an account that has the required permissions',
          action: () => this.onLogin?.(),
          primary: true
        });
        break;

      default:
        if (error.isRetryable) {
          actions.push({
            type: 'retry',
            label: 'Try Again',
            description: 'Attempt the operation again',
            action: () => {}, // Will be set by retry handler
            primary: true
          });
        }
        break;
    }

    // Always add contact support option for persistent issues
    if (error.retryCount && error.retryCount >= this.retryConfig.maxAttempts - 1) {
      actions.push({
        type: 'contact_support',
        label: 'Contact Support',
        description: 'Get help from our support team',
        action: () => this.onContactSupport?.(),
        primary: false
      });
    }

    // Always add dismiss option
    actions.push({
      type: 'dismiss',
      label: 'Dismiss',
      description: 'Close this error message',
      action: () => {}, // Will be set by error handler
      primary: false
    });

    return actions;
  }

  /**
   * Calculate retry delay with exponential backoff
   */
  calculateRetryDelay(retryCount: number): number {
    const delay = Math.min(
      this.retryConfig.baseDelay * Math.pow(this.retryConfig.backoffMultiplier, retryCount),
      this.retryConfig.maxDelay
    );
    
    // Add jitter to prevent thundering herd
    const jitter = Math.random() * 0.1 * delay;
    return Math.floor(delay + jitter);
  }

  /**
   * Execute a function with automatic retry logic for transient failures
   */
  async withRetry<T>(
    operation: () => Promise<T>,
    context: ErrorContext = {},
    customRetryConfig?: Partial<RetryConfig>
  ): Promise<T> {
    const config = { ...this.retryConfig, ...customRetryConfig };
    let lastError: EnhancedAuthError | null = null;
    
    for (let attempt = 0; attempt < config.maxAttempts; attempt++) {
      try {
        return await operation();
      } catch (error) {
        lastError = this.processError(error, {
          ...context,
          operation: context.operation || 'retry_operation'
        });
        
        lastError.retryCount = attempt + 1;

        // If this is the last attempt or error is not retryable, throw
        if (attempt === config.maxAttempts - 1 || !lastError.isRetryable) {
          throw lastError;
        }

        // Calculate delay for next retry
        const delay = this.calculateRetryDelay(attempt);
        lastError.nextRetryAt = new Date(Date.now() + delay);

        console.log(
          `Retry attempt ${attempt + 1}/${config.maxAttempts} for ${lastError.error}. ` +
          `Waiting ${delay}ms before next attempt.`
        );

        // Wait before retrying
        await new Promise(resolve => setTimeout(resolve, delay));
      }
    }

    // This should never be reached, but TypeScript requires it
    throw lastError || new Error('Retry operation failed');
  }

  /**
   * Get user-friendly error message
   */
  getUserFriendlyMessage(error: EnhancedAuthError): string {
    const errorInfo = ERROR_MESSAGES[error.error] || ERROR_MESSAGES.UNKNOWN_ERROR;
    return `${errorInfo.title}: ${errorInfo.message} ${errorInfo.suggestion}`;
  }

  /**
   * Log error for monitoring and debugging
   */
  logError(error: EnhancedAuthError): void {
    const logData = {
      error: error.error,
      message: error.message,
      context: error.context,
      retryCount: error.retryCount,
      timestamp: new Date().toISOString(),
      userAgent: error.context?.userAgent,
      url: error.context?.url,
      operation: error.context?.operation
    };

    // Log to console in development
    if (process.env.NODE_ENV === 'development') {
      console.error('Authentication Error:', logData);
    }

    // In production, send to monitoring service
    try {
      // Example: Send to error tracking service
      // errorTrackingService.captureException(new Error(error.message), {
      //   tags: { errorType: error.error },
      //   extra: logData
      // });
    } catch (e) {
      console.error('Failed to log error to monitoring service:', e);
    }
  }
}

/**
 * Create a default error handler instance
 */
export function createAuthErrorHandler(
  config?: Partial<RetryConfig>,
  callbacks?: {
    onLogin?: () => void;
    onRefresh?: () => Promise<void>;
    onContactSupport?: () => void;
  }
): AuthErrorHandler {
  return new AuthErrorHandler(config, callbacks);
}

/**
 * Utility function to check if an error is an authentication error
 */
export function isAuthenticationError(error: any): boolean {
  if (!error) return false;
  
  const authErrorTypes = [
    'TOKEN_EXPIRED',
    'TOKEN_INVALID', 
    'TOKEN_MISSING',
    'TOKEN_REFRESH_FAILED',
    'AUTHENTICATION_ERROR',
    'AUTHORIZATION_ERROR'
  ];
  
  return authErrorTypes.includes(error.error) || 
         error.status === 401 || 
         error.status === 403;
}

/**
 * Utility function to check if an error is retryable
 */
export function isRetryableError(error: any): boolean {
  if (!error) return false;
  
  return DEFAULT_RETRY_CONFIG.retryableErrors.includes(error.error) ||
         error.status === 429 || // Rate limit
         error.status === 503 || // Service unavailable
         error.status === 502 || // Bad gateway
         error.status === 504;   // Gateway timeout
}

/**
 * Format error for display in UI components
 */
export function formatErrorForDisplay(error: EnhancedAuthError): {
  title: string;
  message: string;
  suggestion: string;
  actions: ErrorRecoveryAction[];
} {
  const errorInfo = ERROR_MESSAGES[error.error] || ERROR_MESSAGES.UNKNOWN_ERROR;
  
  return {
    title: errorInfo.title,
    message: errorInfo.message,
    suggestion: errorInfo.suggestion,
    actions: error.recoveryActions || []
  };
}