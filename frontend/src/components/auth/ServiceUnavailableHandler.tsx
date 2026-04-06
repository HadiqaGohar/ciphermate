'use client';

import React, { useState, useEffect } from 'react';
import { checkAuth0ServiceAvailability } from '../../lib/auth-utils';

interface ServiceUnavailableHandlerProps {
  onServiceRestored?: () => void;
  showRetryButton?: boolean;
  autoRetryInterval?: number; // in milliseconds
  maxAutoRetries?: number;
}

export function ServiceUnavailableHandler({
  onServiceRestored,
  showRetryButton = true,
  autoRetryInterval = 60000, // 1 minute
  maxAutoRetries = 5
}: ServiceUnavailableHandlerProps) {
  const [isVisible, setIsVisible] = useState(false);
  const [isChecking, setIsChecking] = useState(false);
  const [retryCount, setRetryCount] = useState(0);
  const [nextRetryIn, setNextRetryIn] = useState<number | null>(null);

  useEffect(() => {
    const handleServiceUnavailable = (event: CustomEvent) => {
      console.log('Auth0 service unavailable event received:', event.detail);
      setIsVisible(true);
      setRetryCount(0);
      
      // Start auto-retry if enabled
      if (autoRetryInterval > 0 && maxAutoRetries > 0) {
        startAutoRetry();
      }
    };

    // Listen for service unavailable events
    window.addEventListener('auth0ServiceUnavailable', handleServiceUnavailable as EventListener);

    return () => {
      window.removeEventListener('auth0ServiceUnavailable', handleServiceUnavailable as EventListener);
    };
  }, [autoRetryInterval, maxAutoRetries]);

  const startAutoRetry = () => {
    if (retryCount >= maxAutoRetries) {
      console.log('Max auto-retries reached for service availability check');
      return;
    }

    setNextRetryIn(autoRetryInterval / 1000); // Convert to seconds for display

    // Countdown timer
    const countdownInterval = setInterval(() => {
      setNextRetryIn(prev => {
        if (prev === null || prev <= 1) {
          clearInterval(countdownInterval);
          return null;
        }
        return prev - 1;
      });
    }, 1000);

    // Auto-retry after interval
    setTimeout(async () => {
      clearInterval(countdownInterval);
      await checkServiceAvailability();
    }, autoRetryInterval);
  };

  const checkServiceAvailability = async () => {
    setIsChecking(true);
    setRetryCount(prev => prev + 1);

    try {
      const isAvailable = await checkAuth0ServiceAvailability();
      
      if (isAvailable) {
        console.log('✅ Auth0 service is now available');
        setIsVisible(false);
        setRetryCount(0);
        setNextRetryIn(null);
        onServiceRestored?.();
      } else {
        console.log('Auth0 service is still unavailable');
        
        // Continue auto-retry if we haven't reached the limit
        if (retryCount < maxAutoRetries) {
          startAutoRetry();
        }
      }
    } catch (error) {
      console.error('Error checking service availability:', error);
      
      // Continue auto-retry on error if we haven't reached the limit
      if (retryCount < maxAutoRetries) {
        startAutoRetry();
      }
    } finally {
      setIsChecking(false);
    }
  };

  const handleManualRetry = () => {
    setRetryCount(0); // Reset retry count for manual retry
    checkServiceAvailability();
  };

  const handleDismiss = () => {
    setIsVisible(false);
    setRetryCount(0);
    setNextRetryIn(null);
  };

  if (!isVisible) {
    return null;
  }

  return (
    <div className="fixed top-0 left-0 right-0 z-50 bg-yellow-50 border-b border-yellow-200 p-4">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-start">
          <div className="flex-shrink-0">
            <span className="text-2xl" role="img" aria-label="Service status">
              {isChecking ? '🔄' : '⚠️'}
            </span>
          </div>
          
          <div className="ml-3 flex-1">
            <h3 className="text-sm font-medium text-yellow-800">
              Authentication Service Temporarily Unavailable
            </h3>
            
            <div className="mt-2 text-sm text-yellow-700">
              <p>
                The authentication service is currently experiencing issues. 
                Some features may be limited until the service is restored.
              </p>
              
              {isChecking && (
                <p className="mt-1 text-yellow-600">
                  Checking service status...
                </p>
              )}
              
              {nextRetryIn !== null && nextRetryIn > 0 && (
                <p className="mt-1 text-yellow-600">
                  Automatic retry in {nextRetryIn} seconds... (Attempt {retryCount + 1}/{maxAutoRetries})
                </p>
              )}
              
              {retryCount >= maxAutoRetries && (
                <p className="mt-1 text-yellow-600">
                  Automatic retries exhausted. You can try manually or wait for the service to be restored.
                </p>
              )}
            </div>

            <div className="mt-4 flex flex-wrap gap-2">
              {showRetryButton && (
                <button
                  onClick={handleManualRetry}
                  disabled={isChecking}
                  className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-yellow-600 hover:bg-yellow-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {isChecking ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Checking...
                    </>
                  ) : (
                    'Check Again'
                  )}
                </button>
              )}

              <button
                onClick={handleDismiss}
                className="inline-flex items-center px-3 py-2 border border-gray-300 text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500"
              >
                Dismiss
              </button>
            </div>

            {/* Status Information */}
            <div className="mt-4 text-xs text-gray-600">
              <div className="flex items-center space-x-4">
                <span>Status: {isChecking ? 'Checking...' : 'Unavailable'}</span>
                <span>Retry Count: {retryCount}/{maxAutoRetries}</span>
                {nextRetryIn !== null && nextRetryIn > 0 && (
                  <span>Next Check: {nextRetryIn}s</span>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

// Hook for using service unavailability handler
export function useServiceUnavailabilityHandler() {
  const [isServiceUnavailable, setIsServiceUnavailable] = useState(false);

  useEffect(() => {
    const handleServiceUnavailable = () => {
      setIsServiceUnavailable(true);
    };

    const handleServiceRestored = () => {
      setIsServiceUnavailable(false);
    };

    window.addEventListener('auth0ServiceUnavailable', handleServiceUnavailable);
    window.addEventListener('auth0ServiceRestored', handleServiceRestored);

    return () => {
      window.removeEventListener('auth0ServiceUnavailable', handleServiceUnavailable);
      window.removeEventListener('auth0ServiceRestored', handleServiceRestored);
    };
  }, []);

  const triggerServiceUnavailable = () => {
    const event = new CustomEvent('auth0ServiceUnavailable', {
      detail: {
        message: 'Authentication service is temporarily unavailable',
        action: 'retry',
        retryAfter: 60000
      }
    });
    window.dispatchEvent(event);
  };

  const triggerServiceRestored = () => {
    const event = new CustomEvent('auth0ServiceRestored');
    window.dispatchEvent(event);
  };

  return {
    isServiceUnavailable,
    triggerServiceUnavailable,
    triggerServiceRestored
  };
}