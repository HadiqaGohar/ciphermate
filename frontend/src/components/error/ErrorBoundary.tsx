'use client';

import React, { Component, ErrorInfo, ReactNode } from 'react';
import { ErrorFallback } from './ErrorFallback';
import { 
  createAuthErrorHandler, 
  EnhancedAuthError, 
  isAuthenticationError 
} from '../../lib/error-handling';
import { redirectToLogin } from '../../lib/auth-utils';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error | EnhancedAuthError, errorInfo: ErrorInfo) => void;
  onAuthError?: (error: EnhancedAuthError) => void;
  enableRetry?: boolean;
  maxRetries?: number;
}

interface State {
  hasError: boolean;
  error?: Error | EnhancedAuthError;
  errorInfo?: ErrorInfo;
  retryCount: number;
}

export class ErrorBoundary extends Component<Props, State> {
  private errorHandler = createAuthErrorHandler(
    { maxAttempts: this.props.maxRetries || 3 },
    {
      onLogin: () => redirectToLogin(),
      onContactSupport: () => {
        window.open('mailto:support@ciphermate.com?subject=Application Error');
      }
    }
  );

  constructor(props: Props) {
    super(props);
    this.state = { 
      hasError: false, 
      retryCount: 0 
    };
  }

  static getDerivedStateFromError(error: Error): Partial<State> {
    // Update state so the next render will show the fallback UI
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // Process the error with our enhanced error handler
    const enhancedError = this.errorHandler.processError(error, {
      operation: 'component_render',
      url: window.location.href,
      timestamp: new Date().toISOString()
    });

    // Log error for monitoring
    this.errorHandler.logError(enhancedError);
    
    // Call custom error handler if provided
    if (this.props.onError) {
      this.props.onError(enhancedError, errorInfo);
    }

    // Handle authentication errors specifically
    if (isAuthenticationError(enhancedError)) {
      if (this.props.onAuthError) {
        this.props.onAuthError(enhancedError);
      } else {
        // Default auth error handling - redirect to login
        console.log('Authentication error in ErrorBoundary, redirecting to login');
        redirectToLogin();
      }
    }
    
    this.setState({ 
      error: enhancedError, 
      errorInfo,
      retryCount: this.state.retryCount + 1
    });
  }

  private handleRetry = () => {
    const maxRetries = this.props.maxRetries || 3;
    
    if (!this.props.enableRetry || this.state.retryCount >= maxRetries) {
      console.warn('Retry not enabled or max retries exceeded');
      return;
    }

    console.log(`Retrying component render (attempt ${this.state.retryCount + 1}/${maxRetries})`);
    
    this.setState({ 
      hasError: false, 
      error: undefined, 
      errorInfo: undefined 
    });
  };

  private handleReload = () => {
    window.location.reload();
  };

  private handleReset = () => {
    this.setState({ 
      hasError: false, 
      error: undefined, 
      errorInfo: undefined,
      retryCount: 0
    });
  };

  render() {
    if (this.state.hasError) {
      // Custom fallback UI
      if (this.props.fallback) {
        return this.props.fallback;
      }
      
      // Default fallback UI with enhanced error handling
      return (
        <ErrorFallback
          error={this.state.error}
          errorInfo={this.state.errorInfo}
          onRetry={this.props.enableRetry ? this.handleRetry : undefined}
          onReload={this.handleReload}
          onReset={this.handleReset}
          showDetails={process.env.NODE_ENV === 'development'}
        />
      );
    }

    return this.props.children;
  }
}

// Higher-order component for easier usage with enhanced error handling
export function withErrorBoundary<P extends object>(
  Component: React.ComponentType<P>,
  options: {
    fallback?: ReactNode;
    onError?: (error: Error | EnhancedAuthError, errorInfo: ErrorInfo) => void;
    onAuthError?: (error: EnhancedAuthError) => void;
    enableRetry?: boolean;
    maxRetries?: number;
  } = {}
) {
  const WrappedComponent = (props: P) => (
    <ErrorBoundary 
      fallback={options.fallback} 
      onError={options.onError}
      onAuthError={options.onAuthError}
      enableRetry={options.enableRetry}
      maxRetries={options.maxRetries}
    >
      <Component {...props} />
    </ErrorBoundary>
  );
  
  WrappedComponent.displayName = `withErrorBoundary(${Component.displayName || Component.name})`;
  
  return WrappedComponent;
}

// Hook for throwing errors to be caught by error boundary
export function useErrorHandler() {
  const errorHandler = createAuthErrorHandler();

  return React.useCallback((error: Error | any, context?: any) => {
    // Process the error with enhanced information
    const enhancedError = errorHandler.processError(error, {
      operation: 'hook_error',
      ...context
    });

    // Log the error
    errorHandler.logError(enhancedError);

    // Throw the enhanced error to be caught by the nearest error boundary
    throw enhancedError;
  }, [errorHandler]);
}

// Hook for handling async errors that can't be caught by error boundaries
export function useAsyncErrorHandler() {
  const [error, setError] = React.useState<EnhancedAuthError | null>(null);
  const errorHandler = createAuthErrorHandler();

  const handleAsyncError = React.useCallback((error: Error | any, context?: any) => {
    const enhancedError = errorHandler.processError(error, {
      operation: 'async_operation',
      ...context
    });

    // Log the error
    errorHandler.logError(enhancedError);

    // Set error state for component to handle
    setError(enhancedError);

    // Handle authentication errors
    if (isAuthenticationError(enhancedError)) {
      console.log('Async authentication error, redirecting to login');
      redirectToLogin();
    }

    return enhancedError;
  }, [errorHandler]);

  const clearError = React.useCallback(() => {
    setError(null);
  }, []);

  return {
    error,
    handleAsyncError,
    clearError,
    hasError: !!error
  };
}