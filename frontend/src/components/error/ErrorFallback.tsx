'use client';

import React, { ErrorInfo } from 'react';
import { AlertTriangle, RefreshCw, Home, Bug, Clock, Shield } from 'lucide-react';
import { EnhancedAuthError, formatErrorForDisplay, isAuthenticationError } from '../../lib/error-handling';

interface ErrorFallbackProps {
  error?: Error | EnhancedAuthError;
  errorInfo?: ErrorInfo;
  onRetry?: () => void;
  onReload?: () => void;
  onReset?: () => void;
  showDetails?: boolean;
}

export function ErrorFallback({ 
  error, 
  errorInfo, 
  onRetry, 
  onReload,
  onReset,
  showDetails = false 
}: ErrorFallbackProps) {
  const [showErrorDetails, setShowErrorDetails] = React.useState(showDetails);
  const [countdown, setCountdown] = React.useState<number | null>(null);

  // Check if this is an enhanced auth error
  const isEnhancedError = error && 'error' in error && 'details' in error;
  const enhancedError = isEnhancedError ? error as EnhancedAuthError : null;
  const displayInfo = enhancedError ? formatErrorForDisplay(enhancedError) : null;
  const isAuthError = enhancedError ? isAuthenticationError(enhancedError) : false;

  // Handle countdown for retry actions
  React.useEffect(() => {
    if (enhancedError?.nextRetryAt) {
      const updateCountdown = () => {
        const now = Date.now();
        const retryTime = enhancedError.nextRetryAt!.getTime();
        const timeLeft = Math.max(0, retryTime - now);
        
        if (timeLeft > 0) {
          setCountdown(Math.ceil(timeLeft / 1000));
        } else {
          setCountdown(null);
        }
      };

      updateCountdown();
      const interval = setInterval(updateCountdown, 1000);
      return () => clearInterval(interval);
    }
  }, [enhancedError?.nextRetryAt]);

  const handleGoHome = () => {
    window.location.href = '/';
  };

  const handleReportError = () => {
    const errorReport = {
      message: error?.message,
      stack: error instanceof Error ? error.stack : undefined,
      componentStack: errorInfo?.componentStack,
      timestamp: new Date().toISOString(),
      userAgent: navigator.userAgent,
      url: window.location.href,
      errorType: enhancedError?.error,
      context: enhancedError?.context,
    };
    
    console.log('Error report:', errorReport);
    
    const subject = encodeURIComponent('CipherMate Error Report');
    const body = encodeURIComponent(`
Error Details:
- Type: ${enhancedError?.error || 'Unknown'}
- Message: ${error?.message || 'Unknown error'}
- Timestamp: ${new Date().toISOString()}
- URL: ${window.location.href}
- User Agent: ${navigator.userAgent}

Please describe what you were doing when this error occurred:
[Your description here]
    `);
    
    window.open(`mailto:support@ciphermate.com?subject=${subject}&body=${body}`);
  };

  const getErrorIcon = () => {
    if (isAuthError) {
      return <Shield className="w-8 h-8 text-amber-600 dark:text-amber-400" />;
    }
    return <AlertTriangle className="w-8 h-8 text-red-600 dark:text-red-400" />;
  };

  const getErrorIconBg = () => {
    if (isAuthError) {
      return "bg-amber-100 dark:bg-amber-900/20";
    }
    return "bg-red-100 dark:bg-red-900/20";
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
      <div className="max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        {/* Error Icon */}
        <div className="flex justify-center mb-4">
          <div className={`w-16 h-16 ${getErrorIconBg()} rounded-full flex items-center justify-center`}>
            {getErrorIcon()}
          </div>
        </div>

        {/* Error Title */}
        <h1 className="text-xl font-semibold text-gray-900 dark:text-white text-center mb-2">
          {displayInfo?.title || 'Something went wrong'}
        </h1>

        {/* Error Description */}
        <p className="text-gray-600 dark:text-gray-300 text-center mb-4">
          {displayInfo?.message || 'We apologize for the inconvenience. An unexpected error has occurred.'}
        </p>

        {/* Error Suggestion */}
        {displayInfo?.suggestion && (
          <p className="text-sm text-gray-500 dark:text-gray-400 text-center mb-6">
            {displayInfo.suggestion}
          </p>
        )}

        {/* Error Message for non-enhanced errors */}
        {!enhancedError && error?.message && (
          <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md p-3 mb-4">
            <p className="text-sm text-red-800 dark:text-red-200 font-medium">
              {error.message}
            </p>
          </div>
        )}

        {/* Retry Information */}
        {enhancedError?.retryCount && enhancedError.retryCount > 0 && (
          <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-md p-3 mb-4">
            <div className="flex items-center">
              <Clock className="w-4 h-4 text-blue-600 dark:text-blue-400 mr-2" />
              <p className="text-sm text-blue-800 dark:text-blue-200">
                Attempt {enhancedError.retryCount} failed
                {countdown && countdown > 0 && (
                  <span className="ml-2">• Retry in {countdown}s</span>
                )}
              </p>
            </div>
          </div>
        )}

        {/* Recovery Actions */}
        <div className="space-y-3 mb-4">
          {displayInfo?.actions.map((action, index) => (
            <button
              key={index}
              onClick={() => {
                switch (action.type) {
                  case 'retry':
                    onRetry?.();
                    break;
                  case 'dismiss':
                    onReset?.();
                    break;
                  default:
                    action.action();
                    break;
                }
              }}
              disabled={action.disabled || (action.countdown ? action.countdown > 0 : false)}
              className={`
                w-full flex items-center justify-center px-4 py-2 rounded-md transition-colors
                ${action.primary
                  ? 'bg-blue-600 hover:bg-blue-700 text-white'
                  : 'bg-gray-200 hover:bg-gray-300 dark:bg-gray-600 dark:hover:bg-gray-500 text-gray-900 dark:text-white'
                }
                disabled:opacity-50 disabled:cursor-not-allowed
              `}
            >
              {action.countdown && action.countdown > 0 ? (
                <>
                  <Clock className="w-4 h-4 mr-2" />
                  {action.label} ({Math.ceil(action.countdown / 1000)}s)
                </>
              ) : (
                <>
                  {action.type === 'retry' && <RefreshCw className="w-4 h-4 mr-2" />}
                  {action.type === 'login' && <Shield className="w-4 h-4 mr-2" />}
                  {action.label}
                </>
              )}
            </button>
          ))}

          {/* Fallback actions for non-enhanced errors */}
          {!enhancedError && (
            <>
              {onRetry && (
                <button
                  onClick={onRetry}
                  className="w-full flex items-center justify-center px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Try Again
                </button>
              )}
              
              {onReload && (
                <button
                  onClick={onReload}
                  className="w-full flex items-center justify-center px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
                >
                  <RefreshCw className="w-4 h-4 mr-2" />
                  Reload Page
                </button>
              )}
              
              <button
                onClick={handleGoHome}
                className="w-full flex items-center justify-center px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-md transition-colors"
              >
                <Home className="w-4 h-4 mr-2" />
                Go to Home
              </button>
            </>
          )}
        </div>

        {/* Error Details Toggle */}
        {(error || errorInfo) && (
          <div className="border-t border-gray-200 dark:border-gray-700 pt-4">
            <button
              onClick={() => setShowErrorDetails(!showErrorDetails)}
              className="text-sm text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 transition-colors"
            >
              {showErrorDetails ? 'Hide' : 'Show'} Error Details
            </button>
            
            {showErrorDetails && (
              <div className="mt-3 p-3 bg-gray-100 dark:bg-gray-700 rounded-md">
                <div className="text-xs font-mono text-gray-800 dark:text-gray-200 space-y-2">
                  {enhancedError && (
                    <div>
                      <strong>Error Type:</strong> {enhancedError.error}
                      <br />
                      <strong>Technical Details:</strong> {enhancedError.technicalDetails}
                      {enhancedError.context && (
                        <>
                          <br />
                          <strong>Context:</strong>
                          <pre className="whitespace-pre-wrap mt-1 text-xs">
                            {JSON.stringify(enhancedError.context, null, 2)}
                          </pre>
                        </>
                      )}
                    </div>
                  )}
                  
                  {error instanceof Error && error.stack && (
                    <div>
                      <strong>Stack Trace:</strong>
                      <pre className="whitespace-pre-wrap mt-1 text-xs">
                        {error.stack}
                      </pre>
                    </div>
                  )}
                  
                  {errorInfo?.componentStack && (
                    <div>
                      <strong>Component Stack:</strong>
                      <pre className="whitespace-pre-wrap mt-1 text-xs">
                        {errorInfo.componentStack}
                      </pre>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Report Error Button */}
        <div className="border-t border-gray-200 dark:border-gray-700 pt-4 mt-4">
          <button
            onClick={handleReportError}
            className="w-full flex items-center justify-center px-4 py-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
          >
            <Bug className="w-4 h-4 mr-2" />
            Report This Error
          </button>
        </div>
      </div>
    </div>
  );
}

// Enhanced simple error fallback for smaller components
export function SimpleErrorFallback({ 
  error, 
  onRetry 
}: { 
  error?: Error | EnhancedAuthError; 
  onRetry?: () => void; 
}) {
  const isEnhancedError = error && 'error' in error && 'details' in error;
  const enhancedError = isEnhancedError ? error as EnhancedAuthError : null;
  const displayInfo = enhancedError ? formatErrorForDisplay(enhancedError) : null;
  const isAuthError = enhancedError ? isAuthenticationError(enhancedError) : false;

  const getIconColor = () => {
    if (isAuthError) return "text-amber-400";
    return "text-red-400";
  };

  const getBorderColor = () => {
    if (isAuthError) return "border-amber-200 dark:border-amber-800";
    return "border-red-200 dark:border-red-800";
  };

  const getBgColor = () => {
    if (isAuthError) return "bg-amber-50 dark:bg-amber-900/20";
    return "bg-red-50 dark:bg-red-900/20";
  };

  const getTextColor = () => {
    if (isAuthError) return "text-amber-800 dark:text-amber-200";
    return "text-red-800 dark:text-red-200";
  };

  return (
    <div className={`${getBgColor()} border ${getBorderColor()} rounded-md p-4`}>
      <div className="flex items-start">
        {isAuthError ? (
          <Shield className={`w-5 h-5 ${getIconColor()} mr-3 flex-shrink-0 mt-0.5`} />
        ) : (
          <AlertTriangle className={`w-5 h-5 ${getIconColor()} mr-3 flex-shrink-0 mt-0.5`} />
        )}
        <div className="flex-1">
          <h3 className={`text-sm font-medium ${getTextColor()}`}>
            {displayInfo?.title || 'Something went wrong'}
          </h3>
          <p className={`text-sm ${getTextColor()} mt-1`}>
            {displayInfo?.message || error?.message || 'An unexpected error occurred'}
          </p>
          
          {/* Recovery actions for enhanced errors */}
          {displayInfo?.actions && displayInfo.actions.length > 0 && (
            <div className="mt-3 space-y-2">
              {displayInfo.actions.slice(0, 2).map((action, index) => (
                <button
                  key={index}
                  onClick={() => {
                    if (action.type === 'retry') {
                      onRetry?.();
                    } else {
                      action.action();
                    }
                  }}
                  disabled={action.disabled}
                  className={`text-sm ${getTextColor()} hover:opacity-80 underline mr-4 disabled:opacity-50`}
                >
                  {action.label}
                </button>
              ))}
            </div>
          )}
          
          {/* Fallback retry for non-enhanced errors */}
          {!enhancedError && onRetry && (
            <button
              onClick={onRetry}
              className={`mt-2 text-sm ${getTextColor()} hover:opacity-80 underline`}
            >
              Try again
            </button>
          )}
        </div>
      </div>
    </div>
  );
}