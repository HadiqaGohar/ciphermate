'use client';

import React from 'react';
import { ErrorBoundary } from '../error/ErrorBoundary';
import { SimpleErrorFallback } from '../error/ErrorFallback';
import { EnhancedAuthError } from '../../lib/error-handling';

interface AppErrorBoundaryProps {
  children: React.ReactNode;
}

export function AppErrorBoundary({ children }: AppErrorBoundaryProps) {
  const handleError = (error: Error | EnhancedAuthError, errorInfo: React.ErrorInfo) => {
    // Log error to external service in production
    if (process.env.NODE_ENV === 'production') {
      // Example: Send to error tracking service
      console.error('Application error:', error, errorInfo);
      
      // In a real app, you would send this to an error tracking service like Sentry
      // Sentry.captureException(error, {
      //   contexts: {
      //     react: {
      //       componentStack: errorInfo.componentStack,
      //     },
      //   },
      // });
    }
  };

  return (
    <ErrorBoundary
      onError={handleError}
      fallback={
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex items-center justify-center p-4">
          <div className="max-w-lg w-full">
            <SimpleErrorFallback
              error={new Error('Application error')}
              onRetry={() => window.location.reload()}
            />
          </div>
        </div>
      }
    >
      {children}
    </ErrorBoundary>
  );
}