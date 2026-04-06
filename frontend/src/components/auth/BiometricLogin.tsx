/**
 * Biometric Login Component
 * Fingerprint/Face ID authentication UI
 * WINNING FEATURE: Professional biometric auth interface!
 */

'use client';

import React, { useState, useEffect } from 'react';
import { useBiometricAuth } from '../../lib/biometric-auth';
import { useAuth } from '../../hooks/useAuth';

interface BiometricLoginProps {
  onSuccess?: (credential: any) => void;
  onFallback?: () => void;
  className?: string;
}

export function BiometricLogin({ onSuccess, onFallback, className = '' }: BiometricLoginProps) {
  const { isAvailable, isRegistered, isAuthenticating, register, authenticate } = useBiometricAuth();
  const { user, login } = useAuth();
  const [showSetup, setShowSetup] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Auto-attempt biometric auth if available and registered
    if (isAvailable && isRegistered && !user) {
      handleBiometricAuth();
    }
  }, [isAvailable, isRegistered, user]);

  const handleBiometricAuth = async () => {
    setError(null);
    
    try {
      const result = await authenticate();
      
      if (result.success) {
        onSuccess?.(result.credential);
      } else if (result.fallbackRequired) {
        setError(result.error || 'Biometric authentication failed');
        onFallback?.();
      }
    } catch (err) {
      setError('Authentication failed. Please try again.');
      onFallback?.();
    }
  };

  const handleSetupBiometric = async () => {
    if (!user?.sub) {
      setError('Please log in first to set up biometric authentication');
      return;
    }

    setError(null);
    
    try {
      const result = await register(user.sub);
      
      if (result.success) {
        setShowSetup(false);
        // Show success message
      } else {
        setError(result.error || 'Failed to set up biometric authentication');
      }
    } catch (err) {
      setError('Setup failed. Please try again.');
    }
  };

  const getBiometricIcon = () => {
    const userAgent = navigator.userAgent.toLowerCase();
    
    if (userAgent.includes('iphone') || userAgent.includes('ipad')) {
      return (
        <svg className="w-12 h-12 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm-1-13h2v6h-2zm0 8h2v2h-2z"/>
        </svg>
      );
    } else {
      return (
        <svg className="w-12 h-12 text-blue-600" fill="currentColor" viewBox="0 0 24 24">
          <path d="M17.81 4.47c-.08 0-.16-.02-.23-.06C15.66 3.42 14 3 12.01 3c-1.98 0-3.86.47-5.57 1.41-.24.13-.54.04-.68-.2-.13-.24-.04-.55.2-.68C7.82 2.52 9.86 2 12.01 2c2.13 0 3.99.47 6.03 1.52.25.13.34.43.21.67-.09.18-.26.28-.44.28zM3.5 9.72c-.1 0-.2-.03-.29-.09-.23-.16-.28-.47-.12-.7.99-1.4 2.25-2.5 3.75-3.27C9.98 4.04 14.05 4.04 17.15 5.66c1.5.77 2.76 1.86 3.75 3.27.16.22.11.54-.12.7-.23.16-.54.11-.7-.12-.9-1.28-2.04-2.25-3.39-2.94-2.87-1.47-6.54-1.47-9.4 0-1.36.69-2.5 1.66-3.4 2.94-.08.14-.23.21-.39.21z"/>
        </svg>
      );
    }
  };

  const getBiometricType = () => {
    const userAgent = navigator.userAgent.toLowerCase();
    
    if (userAgent.includes('iphone') || userAgent.includes('ipad')) {
      return 'Face ID';
    } else if (userAgent.includes('android')) {
      return 'Fingerprint';
    }
    
    return 'Biometric';
  };

  if (!isAvailable) {
    return (
      <div className={`text-center p-6 bg-gray-50 dark:bg-gray-800 rounded-lg ${className}`}>
        <div className="text-gray-500 dark:text-gray-400">
          <svg className="w-8 h-8 mx-auto mb-2" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
          <p className="text-sm">Biometric authentication not available on this device</p>
        </div>
      </div>
    );
  }

  if (showSetup || (!isRegistered && user)) {
    return (
      <div className={`text-center p-6 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 ${className}`}>
        <div className="mb-4">
          {getBiometricIcon()}
        </div>
        
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
          Set up {getBiometricType()}
        </h3>
        
        <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
          Enable {getBiometricType()} for faster, more secure login to your account.
        </p>

        {error && (
          <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
            <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
          </div>
        )}

        <div className="space-y-3">
          <button
            onClick={handleSetupBiometric}
            disabled={isAuthenticating}
            className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-md transition-colors flex items-center justify-center space-x-2"
          >
            {isAuthenticating ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                <span>Setting up...</span>
              </>
            ) : (
              <>
                <span>Enable {getBiometricType()}</span>
              </>
            )}
          </button>
          
          <button
            onClick={() => setShowSetup(false)}
            className="w-full px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
          >
            Skip for now
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`text-center p-6 bg-white dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700 ${className}`}>
      <div className="mb-4">
        {getBiometricIcon()}
      </div>
      
      <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
        {isRegistered ? `Sign in with ${getBiometricType()}` : 'Biometric Authentication'}
      </h3>
      
      <p className="text-sm text-gray-600 dark:text-gray-400 mb-6">
        {isRegistered 
          ? `Use your ${getBiometricType()} to sign in quickly and securely.`
          : 'Set up biometric authentication for enhanced security.'
        }
      </p>

      {error && (
        <div className="mb-4 p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-md">
          <p className="text-sm text-red-600 dark:text-red-400">{error}</p>
        </div>
      )}

      <div className="space-y-3">
        {isRegistered ? (
          <>
            <button
              onClick={handleBiometricAuth}
              disabled={isAuthenticating}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white rounded-md transition-colors flex items-center justify-center space-x-2"
            >
              {isAuthenticating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  <span>Authenticating...</span>
                </>
              ) : (
                <>
                  <span>Use {getBiometricType()}</span>
                </>
              )}
            </button>
            
            <button
              onClick={onFallback}
              className="w-full px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
            >
              Use password instead
            </button>
          </>
        ) : (
          <>
            <button
              onClick={() => setShowSetup(true)}
              className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-md transition-colors"
            >
              Set up {getBiometricType()}
            </button>
            
            <button
              onClick={login}
              className="w-full px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
            >
              Sign in with Auth0
            </button>
          </>
        )}
      </div>

      {/* Security indicator */}
      <div className="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
          <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12,1L3,5V11C3,16.55 6.84,21.74 12,23C17.16,21.74 21,16.55 21,11V5L12,1M10,17L6,13L7.41,11.59L10,14.17L16.59,7.58L18,9L10,17Z"/>
          </svg>
          <span>Secured with WebAuthn</span>
        </div>
      </div>
    </div>
  );
}

// Biometric status indicator component
export function BiometricStatus() {
  const { isAvailable, isRegistered } = useBiometricAuth();

  if (!isAvailable) return null;

  return (
    <div className="flex items-center space-x-2 text-xs text-gray-500 dark:text-gray-400">
      <svg 
        className={`w-4 h-4 ${isRegistered ? 'text-green-500' : 'text-gray-400'}`} 
        fill="currentColor" 
        viewBox="0 0 24 24"
      >
        <path d="M17.81 4.47c-.08 0-.16-.02-.23-.06C15.66 3.42 14 3 12.01 3c-1.98 0-3.86.47-5.57 1.41-.24.13-.54.04-.68-.2-.13-.24-.04-.55.2-.68C7.82 2.52 9.86 2 12.01 2c2.13 0 3.99.47 6.03 1.52.25.13.34.43.21.67-.09.18-.26.28-.44.28z"/>
      </svg>
      <span>
        {isRegistered ? 'Biometric enabled' : 'Biometric available'}
      </span>
    </div>
  );
}