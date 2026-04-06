'use client';

import React from 'react';
import { useErrorHandler } from '../../hooks/useErrorHandler';
import { useAuth } from '../../hooks/useAuth';
import { SimpleErrorFallback } from '../error/ErrorFallback';

/**
 * Demo component showing comprehensive error handling in action
 */
export function ErrorHandlingDemo() {
  const { handleError, clearError, retry, isError, error, getErrorDisplay } = useErrorHandler({
    retryable: true,
    maxRetries: 3,
    showToast: true,
    logError: true
  });
  
  const { getAccessToken } = useAuth();

  const simulateAuthError = async () => {
    try {
      // Simulate an authentication error
      const mockError = { status: 401, message: 'Token expired' };
      await handleError(mockError, { operation: 'demo_auth_error' });
    } catch (error) {
      console.log('Auth error handled:', error);
    }
  };

  const simulateNetworkError = async () => {
    try {
      // Simulate a network error that should be retryable
      const mockError = new TypeError('fetch failed');
      await handleError(mockError, { operation: 'demo_network_error' });
    } catch (error) {
      console.log('Network error handled:', error);
    }
  };

  const simulateRateLimitError = async () => {
    try {
      // Simulate a rate limit error
      const mockError = { status: 429, message: 'Too many requests' };
      await handleError(mockError, { operation: 'demo_rate_limit' });
    } catch (error) {
      console.log('Rate limit error handled:', error);
    }
  };

  const simulateApiCall = async () => {
    try {
      // Simulate an API call that might fail
      const operation = async () => {
        const token = await getAccessToken();
        if (!token) {
          throw new Error('No access token available');
        }
        
        // Simulate random failure
        if (Math.random() < 0.7) {
          throw new TypeError('Simulated network failure');
        }
        
        return 'API call successful!';
      };

      const result = await retry(operation, { operation: 'demo_api_call' });
      if (result) {
        alert(`Success: ${result}`);
      }
    } catch (error) {
      console.log('API call failed after retries:', error);
    }
  };

  const errorDisplay = error ? getErrorDisplay() : null;

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
          Error Handling Demo
        </h2>
        
        <p className="text-gray-600 dark:text-gray-300 mb-6">
          This demo shows how our comprehensive error handling system works with different types of errors.
        </p>

        {/* Error Display */}
        {isError && error && (
          <div className="mb-6">
            <SimpleErrorFallback 
              error={error} 
              onRetry={() => retry(async () => 'Retry successful!')}
            />
          </div>
        )}

        {/* Demo Buttons */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <button
            onClick={simulateAuthError}
            className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-md transition-colors"
          >
            Simulate Auth Error
          </button>
          
          <button
            onClick={simulateNetworkError}
            className="px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-md transition-colors"
          >
            Simulate Network Error
          </button>
          
          <button
            onClick={simulateRateLimitError}
            className="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 text-white rounded-md transition-colors"
          >
            Simulate Rate Limit
          </button>
          
          <button
            onClick={simulateApiCall}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
          >
            Try API Call (with retry)
          </button>
        </div>

        {/* Clear Error Button */}
        {isError && (
          <button
            onClick={clearError}
            className="px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-md transition-colors"
          >
            Clear Error
          </button>
        )}

        {/* Error Details */}
        {errorDisplay && (
          <div className="mt-6 p-4 bg-gray-50 dark:bg-gray-700 rounded-md">
            <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
              Error Details:
            </h3>
            <div className="text-sm text-gray-600 dark:text-gray-300 space-y-1">
              <p><strong>Title:</strong> {errorDisplay.title}</p>
              <p><strong>Message:</strong> {errorDisplay.message}</p>
              <p><strong>Suggestion:</strong> {errorDisplay.suggestion}</p>
              <p><strong>Actions:</strong> {errorDisplay.actions.map(a => a.label).join(', ')}</p>
            </div>
          </div>
        )}
      </div>

      {/* Feature Overview */}
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">
          Error Handling Features
        </h3>
        
        <ul className="space-y-2 text-sm text-gray-600 dark:text-gray-300">
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Automatic retry logic with exponential backoff for transient failures</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>User-friendly error messages for different failure scenarios</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Authentication error detection and automatic login redirect</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Rate limit handling with countdown timers</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Contextual recovery actions based on error type</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Comprehensive error logging for monitoring and debugging</span>
          </li>
          <li className="flex items-start">
            <span className="text-green-500 mr-2">✓</span>
            <span>Integration with React Error Boundaries for component errors</span>
          </li>
        </ul>
      </div>
    </div>
  );
}