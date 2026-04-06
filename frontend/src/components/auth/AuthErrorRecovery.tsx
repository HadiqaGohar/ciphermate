'use client';

import React, { useState, useEffect } from 'react';
import { 
  EnhancedAuthError, 
  createAuthErrorHandler, 
  formatErrorForDisplay 
} from '../../lib/error-handling';
import { 
  recoverFromAuthError, 
  checkAuth0ServiceAvailability,
  redirectToLogin 
} from '../../lib/auth-utils';

interface AuthErrorRecoveryProps {
  error: EnhancedAuthError;
  onRecovered?: (token: string) => void;
  onDismiss?: () => void;
  onRetry?: () => void;
  showDetails?: boolean;
  autoRetry?: boolean;
  maxAutoRetries?: number;
}

export function AuthErrorRecovery({
  error,
  onRecovered,
  onDismiss,
  onRetry,
  showDetails = false,
  autoRetry = true,
  maxAutoRetries = 2
}: AuthErrorRecoveryProps) {
  const [isRecovering, setIsRecovering] = useState(false);
  const [recoveryAttempts, setRecoveryAttempts] = useState(0);
  const [serviceStatus, setServiceStatus] = useState<'checking' | 'available' | 'unavailable' | null>(null);
  const [countdown, setCountdown] = useState<number | null>(null);

  const errorDisplay = formatErrorForDisplay(error);
  const errorHandler = createAuthErrorHandler();

  // Auto-retry logic for certain error types
  useEffect(() => {
    if (autoRetry && 
        recoveryAttempts < maxAutoRetries && 
        (error.error === 'TOKEN_EXPIRED' || error.error === 'TOKEN_INVALID' || error.error === 'NETWORK_ERROR')) {
      
      const delay = Math.min(1000 * Math.pow(2, recoveryAttempts), 5000); // Exponential backoff, max 5s
      
      console.log(`Auto-retry attempt ${recoveryAttempts + 1} in ${delay}ms for error: ${error.error}`);
      
      const timer = setTimeout(() => {
        handleRecovery();
      }, delay);

      return () => clearTimeout(timer);
    }
  }, [error, recoveryAttempts, autoRetry, maxAutoRetries]);

  // Countdown timer for rate limit errors
  useEffect(() => {
    if (error.error === 'RATE_LIMIT_EXCEEDED' && countdown === null) {
      setCountdown(30); // 30 second countdown
      
      const timer = setInterval(() => {
        setCountdown(prev => {
          if (prev === null || prev <= 1) {
            clearInterval(timer);
            return null;
          }
          return prev - 1;
        });
      }, 1000);

      return () => clearInterval(timer);
    }
  }, [error.error, countdown]);

  const handleRecovery = async () => {
    if (isRecovering) return;

    setIsRecovering(true);
    setRecoveryAttempts(prev => prev + 1);

    try {
      console.log('Starting authentication error recovery...');
      
      // Check service status for service-related errors
      if (error.error === 'AUTH0_SERVICE_ERROR' || error.error === 'NETWORK_ERROR') {
        setServiceStatus('checking');
        const isAvailable = await checkAuth0ServiceAvailability();
        setServiceStatus(isAvailable ? 'available' : 'unavailable');
        
        if (!isAvailable) {
          console.log('Auth0 service is unavailable, cannot recover at this time');
          setIsRecovering(false);
          return;
        }
      }

      // Attempt recovery
      const recoveredToken = await recoverFromAuthError(error, 2);
      
      if (recoveredToken) {
        console.log('✅ Authentication recovery successful');
        onRecovered?.(recoveredToken);
      } else {
        console.log('Authentication recovery failed');
        
        // If we've exhausted auto-retries, show manual options
        if (recoveryAttempts >= maxAutoRetries) {
          console.log('Max auto-retries reached, requiring manual intervention');
        }
      }
    } catch (recoveryError) {
      console.error('Recovery attempt failed:', recoveryError);
      errorHandler.logError(errorHandler.processError(recoveryError));
    } finally {
      setIsRecovering(false);
    }
  };

  const handleManualRetry = () => {
    if (onRetry) {
      onRetry();
    } else {
      handleRecovery();
    }
  };

  const handleLogin = () => {
    redirectToLogin();
  };

  const handleDismiss = () => {
    onDismiss?.();
  };

  const getStatusIcon = () => {
    if (isRecovering) return '🔄';
    
    switch (error.error) {
      case 'TOKEN_EXPIRED':
      case 'TOKEN_INVALID':
        return '🔑';
      case 'AUTH0_SERVICE_ERROR':
        return '🚫';
      case 'NETWORK_ERROR':
        return '📡';
      case 'RATE_LIMIT_EXCEEDED':
        return '⏱️';
      default:
        return '⚠️';
    }
  };

  const getStatusMessage = () => {
    if (isRecovering) {
      return 'Attempting to recover your session...';
    }

    if (serviceStatus === 'checking') {
      return 'Checking authentication service status...';
    }

    if (serviceStatus === 'unavailable') {
      return 'Authentication service is temporarily unavailable. Please try again later.';
    }

    if (countdown !== null && countdown > 0) {
      return `Please wait ${countdown} seconds before trying again.`;
    }

    return errorDisplay.message;
  };

  const canRetry = () => {
    return !isRecovering && 
           serviceStatus !== 'unavailable' && 
           (countdown === null || countdown === 0) &&
           recoveryAttempts < maxAutoRetries + 2; // Allow a few manual retries beyond auto-retries
  };

  const shouldShowRecoveryButton = () => {
    return canRetry() && 
           (error.error === 'TOKEN_EXPIRED' || 
            error.error === 'TOKEN_INVALID' || 
            error.error === 'NETWORK_ERROR' ||
            error.error === 'AUTH0_SERVICE_ERROR');
  };

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
      <div className="flex items-start">
        <div className="flex-shrink-0">
          <span className="text-2xl" role="img" aria-label="Error status">
            {getStatusIcon()}
          </span>
        </div>
        
        <div className="ml-3 flex-1">
          <h3 className="text-sm font-medium text-red-800">
            {errorDisplay.title}
          </h3>
          
          <div className="mt-2 text-sm text-red-700">
            <p>{getStatusMessage()}</p>
            
            {errorDisplay.suggestion && (
              <p className="mt-1 text-red-600">{errorDisplay.suggestion}</p>
            )}
          </div>

          {/* Service Status Indicator */}
          {serviceStatus && (
            <div className="mt-2 text-xs text-gray-600">
              Service Status: {serviceStatus === 'checking' ? 'Checking...' : 
                              serviceStatus === 'available' ? '✅ Available' : 
                              '❌ Unavailable'}
            </div>
          )}

          {/* Recovery Progress */}
          {recoveryAttempts > 0 && (
            <div className="mt-2 text-xs text-gray-600">
              Recovery attempts: {recoveryAttempts}/{maxAutoRetries + 2}
            </div>
          )}

          {/* Action Buttons */}
          <div className="mt-4 flex flex-wrap gap-2">
            {shouldShowRecoveryButton() && (
              <button
                onClick={handleRecovery}
                disabled={!canRetry()}
                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isRecovering ? (
                  <>
                    <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Recovering...
                  </>
                ) : (
                  'Try Recovery'
                )}
              </button>
            )}

            {onRetry && (
              <button
                onClick={handleManualRetry}
                disabled={!canRetry()}
                className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Retry
              </button>
            )}

            <button
              onClick={handleLogin}
              className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Log In Again
            </button>

            {onDismiss && (
              <button
                onClick={handleDismiss}
                className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              >
                Dismiss
              </button>
            )}
          </div>

          {/* Technical Details (Development Only) */}
          {showDetails && (
            <details className="mt-4">
              <summary className="text-xs text-gray-500 cursor-pointer">
                Technical Details
              </summary>
              <div className="mt-2 text-xs text-gray-600 bg-gray-100 p-2 rounded">
                <div><strong>Error Type:</strong> {error.error}</div>
                <div><strong>Message:</strong> {error.message}</div>
                {error.details && (
                  <div><strong>Details:</strong> {JSON.stringify(error.details, null, 2)}</div>
                )}
                {error.context && (
                  <div><strong>Context:</strong> {JSON.stringify(error.context, null, 2)}</div>
                )}
              </div>
            </details>
          )}
        </div>
      </div>
    </div>
  );
}

// Hook for using auth error recovery in components
export function useAuthErrorRecovery() {
  const [error, setError] = useState<EnhancedAuthError | null>(null);
  const [isRecovering, setIsRecovering] = useState(false);

  const handleError = (authError: EnhancedAuthError) => {
    setError(authError);
  };

  const handleRecovered = (token: string) => {
    console.log('Authentication recovered with new token');
    setError(null);
    setIsRecovering(false);
  };

  const handleDismiss = () => {
    setError(null);
    setIsRecovering(false);
  };

  const clearError = () => {
    setError(null);
    setIsRecovering(false);
  };

  return {
    error,
    isRecovering,
    handleError,
    handleRecovered,
    handleDismiss,
    clearError,
    hasError: !!error
  };
}