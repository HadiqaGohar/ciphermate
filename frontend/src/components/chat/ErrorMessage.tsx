'use client';

import { AlertTriangle, X, RefreshCw, ExternalLink, Clock } from 'lucide-react';
import { ApiError } from '../../lib/api-client';
import { EnhancedAuthError } from '../../lib/error-handling';

interface ErrorMessageProps {
  message?: string;
  error?: ApiError | EnhancedAuthError;
  onDismiss: () => void;
  onRetry?: () => void;
  showDetails?: boolean;
  className?: string;
}

export function ErrorMessage({ 
  message, 
  error, 
  onDismiss, 
  onRetry,
  showDetails = false,
  className = ''
}: ErrorMessageProps) {
  const errorMessage = error?.message || message || 'An error occurred';
  
  // Handle different error types
  const isApiError = (err: any): err is ApiError => {
    return err && 'name' in err && err.name === 'ApiError';
  };
  
  const isEnhancedAuthError = (err: any): err is EnhancedAuthError => {
    return err && 'error' in err && typeof err.error === 'string';
  };
  
  const userAction = undefined; // ApiError doesn't have user_action, only EnhancedAuthError might have recovery actions

  const getErrorSeverity = () => {
    if (!error) return 'error';
    
    if (isEnhancedAuthError(error)) {
      switch (error.error) {
        case 'RATE_LIMIT_EXCEEDED':
        case 'AUTH0_SERVICE_ERROR':
          return 'warning';
        case 'TOKEN_EXPIRED':
        case 'TOKEN_INVALID':
          return 'info';
        default:
          return 'error';
      }
    }
    
    if (isApiError(error)) {
      switch (error.status) {
        case 429: // Rate limit
        case 503: // Service unavailable
          return 'warning';
        case 400: // Bad request / validation
          return 'info';
        default:
          return 'error';
      }
    }
    
    return 'error';
  };

  const severity = getErrorSeverity();
  
  const severityStyles = {
    error: {
      bg: 'bg-red-50 dark:bg-red-900/20',
      border: 'border-red-200 dark:border-red-800',
      icon: 'text-red-400',
      title: 'text-red-800 dark:text-red-200',
      text: 'text-red-700 dark:text-red-300',
      button: 'text-red-800 dark:text-red-200 hover:text-red-900 dark:hover:text-red-100'
    },
    warning: {
      bg: 'bg-yellow-50 dark:bg-yellow-900/20',
      border: 'border-yellow-200 dark:border-yellow-800',
      icon: 'text-yellow-400',
      title: 'text-yellow-800 dark:text-yellow-200',
      text: 'text-yellow-700 dark:text-yellow-300',
      button: 'text-yellow-800 dark:text-yellow-200 hover:text-yellow-900 dark:hover:text-yellow-100'
    },
    info: {
      bg: 'bg-blue-50 dark:bg-blue-900/20',
      border: 'border-blue-200 dark:border-blue-800',
      icon: 'text-blue-400',
      title: 'text-blue-800 dark:text-blue-200',
      text: 'text-blue-700 dark:text-blue-300',
      button: 'text-blue-800 dark:text-blue-200 hover:text-blue-900 dark:hover:text-blue-100'
    }
  };

  const styles = severityStyles[severity];

  const renderActionButton = () => {
    // For now, just show retry button if onRetry is available
    if (onRetry) {
      return (
        <button
          onClick={onRetry}
          className={`inline-flex items-center px-3 py-1 text-sm font-medium ${styles.button} bg-white dark:bg-gray-800 border border-current rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors`}
        >
          <RefreshCw className="w-4 h-4 mr-1" />
          Try Again
        </button>
      );
    }
    
    return null;
  };

  const renderSuggestions = () => {
    // For EnhancedAuthError, show recovery actions as suggestions
    if (isEnhancedAuthError(error) && error.recoveryActions?.length) {
      return (
        <div className="mt-3">
          <p className={`text-sm font-medium ${styles.title} mb-2`}>
            Available Actions:
          </p>
          <div className="flex flex-wrap gap-2">
            {error.recoveryActions.map((action, index) => (
              <button
                key={index}
                onClick={action.action}
                disabled={action.disabled}
                className={`inline-flex items-center px-3 py-1 text-sm font-medium ${styles.button} bg-white dark:bg-gray-800 border border-current rounded-md hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed`}
              >
                {action.label}
              </button>
            ))}
          </div>
        </div>
      );
    }
    
    return null;
  };

  const renderErrorDetails = () => {
    if (!showDetails || !error) return null;

    return (
      <details className="mt-3">
        <summary className={`text-sm ${styles.button} cursor-pointer hover:underline`}>
          Technical Details
        </summary>
        <div className="mt-2 p-3 bg-gray-100 dark:bg-gray-700 rounded-md">
          <dl className="text-xs space-y-1">
            <div>
              <dt className="font-semibold text-gray-600 dark:text-gray-300">Error Code:</dt>
              <dd className="text-gray-800 dark:text-gray-200">
                {isEnhancedAuthError(error) ? error.error : isApiError(error) ? `HTTP_${error.status}` : 'UNKNOWN'}
              </dd>
            </div>
            {isApiError(error) && (
              <div>
                <dt className="font-semibold text-gray-600 dark:text-gray-300">Status:</dt>
                <dd className="text-gray-800 dark:text-gray-200">{error.status} {error.statusText}</dd>
              </div>
            )}
            <div>
              <dt className="font-semibold text-gray-600 dark:text-gray-300">Timestamp:</dt>
              <dd className="text-gray-800 dark:text-gray-200">
                {isEnhancedAuthError(error) && error.context?.timestamp
                  ? new Date(error.context.timestamp).toLocaleString()
                  : new Date().toLocaleString()
                }
              </dd>
            </div>
            {isEnhancedAuthError(error) && error.details && (
              <div>
                <dt className="font-semibold text-gray-600 dark:text-gray-300">Details:</dt>
                <dd className="text-gray-800 dark:text-gray-200">
                  <pre className="whitespace-pre-wrap text-xs">
                    {JSON.stringify(error.details, null, 2)}
                  </pre>
                </dd>
              </div>
            )}
          </dl>
        </div>
      </details>
    );
  };

  return (
    <div className={`${styles.bg} ${styles.border} border rounded-md p-4 ${className}`}>
      <div className="flex items-start">
        <AlertTriangle className={`w-5 h-5 ${styles.icon} mr-3 flex-shrink-0 mt-0.5`} />
        
        <div className="flex-1 min-w-0">
          <h4 className={`text-sm font-medium ${styles.title} mb-1`}>
            {severity === 'error' ? 'Error' : severity === 'warning' ? 'Warning' : 'Information'}
          </h4>
          
          <p className={`text-sm ${styles.text} mb-3`}>
            {errorMessage}
          </p>

          <div className="flex items-center gap-3">
            {renderActionButton()}
          </div>

          {renderSuggestions()}
          {renderErrorDetails()}
        </div>

        <button
          onClick={onDismiss}
          className={`ml-3 ${styles.icon} hover:text-opacity-75 transition-colors flex-shrink-0`}
          aria-label="Dismiss error"
        >
          <X className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}